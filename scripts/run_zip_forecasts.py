#!/usr/bin/env python3
"""Run IFP forecasts by congressional district zip lists from an Excel file."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_API_URL = (
    "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast"
)
DEFAULT_SOURCE = "RYM Frequency Cap Test"
INCLUDE = "com.disney.digital.ads.rule.manager.common.Include"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def zips_from_column(series) -> list[str]:
    return [str(int(value)).zfill(5) for value in series.dropna()]


def apply_postal_codes(body: dict[str, Any], postal_codes: list[str]) -> dict[str, Any]:
    payload = copy.deepcopy(body)
    term_list = payload["targeting-detail"]["targeting-rules"][0]["definition"]["term-list"]
    term_list[:] = [term for term in term_list if term.get("dimension") != "postal-code"]
    term_list.append(
        {
            "sub-class": INCLUDE,
            "dimension": "postal-code",
            "value-set": postal_codes,
            "not": False,
            "supported": True,
        }
    )
    return payload


def aggregate_monthly(daily_details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_month: dict[str, dict[str, int]] = {}
    for day in daily_details:
        month = day["date"][:7]
        bucket = by_month.setdefault(month, {"capacity": 0, "available": 0})
        bucket["capacity"] += int(day["capacity"])
        bucket["available"] += int(day["available"])

    monthly: list[dict[str, Any]] = []
    for month in sorted(by_month):
        capacity = by_month[month]["capacity"]
        available = by_month[month]["available"]
        ratio = None if not capacity else round(float(available) / float(capacity), 6)
        monthly.append(
            {
                "month": month,
                "capacity": capacity,
                "available": available,
                "ratio": ratio,
            }
        )
    return monthly


def post_forecast(api_url: str, source: str, body: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        api_url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Source": source,
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def run_case(
    base_request: dict[str, Any],
    district: str,
    postal_codes: list[str],
    start_date: str,
    end_date: str,
    api_url: str,
    source: str,
    timeout: int,
) -> dict[str, Any]:
    body = apply_postal_codes(base_request, postal_codes)
    body["start-date"] = start_date
    body["end-date"] = end_date
    response = post_forecast(api_url, source, body, timeout)
    summary = response["summary"]
    capacity = summary["capacity"]
    available = summary["available"]
    ratio = None if not capacity else round(float(available) / float(capacity), 6)
    return {
        "district": district,
        "zip_count": len(postal_codes),
        "start_date": start_date,
        "end_date": end_date,
        "capacity": capacity,
        "available": available,
        "ratio": ratio,
        "monthly_details": aggregate_monthly(response.get("daily-details", [])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run IFP forecasts for zip lists by district")
    parser.add_argument("--excel", type=Path, required=True, help="Excel file with district columns")
    parser.add_argument(
        "--base-request",
        type=Path,
        default=Path("config/base-request.json"),
        help="Base forecast request body",
    )
    parser.add_argument("--start-date", default="2026-08-10")
    parser.add_argument("--end-date", default="2026-12-31")
    parser.add_argument("--output-json", type=Path, default=Path("output/gmmb-zip-forecasts.json"))
    parser.add_argument("--output-csv", type=Path, default=Path("output/gmmb-zip-forecasts.csv"))
    parser.add_argument(
        "--output-monthly-csv",
        type=Path,
        default=Path("output/gmmb-zip-forecasts-monthly.csv"),
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("IFP_API_URL", DEFAULT_API_URL),
    )
    parser.add_argument(
        "--source",
        default=os.getenv("IFP_SOURCE_HEADER", DEFAULT_SOURCE),
    )
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("pandas and openpyxl are required: py -m pip install pandas openpyxl", file=sys.stderr)
        return 1

    base_request = load_json(args.base_request)
    df = pd.read_excel(args.excel)

    results: list[dict[str, Any]] = []
    for district in df.columns:
        postal_codes = zips_from_column(df[district])
        if not postal_codes:
            continue
        print(f"Running {district} ({len(postal_codes)} zips)...", flush=True)
        try:
            results.append(
                run_case(
                    base_request,
                    district,
                    postal_codes,
                    args.start_date,
                    args.end_date,
                    args.api_url,
                    args.source,
                    args.timeout,
                )
            )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            print(f"  FAILED {district}: HTTP {exc.code} {detail}", file=sys.stderr)
            results.append(
                {
                    "district": district,
                    "zip_count": len(postal_codes),
                    "error": f"HTTP {exc.code}: {detail}",
                }
            )

    all_zips = sorted(
        {
            str(int(value)).zfill(5)
            for district in df.columns
            for value in df[district].dropna()
        }
    )
    print(f"Running ALL ({len(all_zips)} unique zips)...", flush=True)
    try:
        combined = run_case(
            base_request,
            "ALL",
            all_zips,
            args.start_date,
            args.end_date,
            args.api_url,
            args.source,
            args.timeout,
        )
        results.append(combined)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        print(f"  FAILED ALL: HTTP {exc.code} {detail}", file=sys.stderr)
        results.append({"district": "ALL", "zip_count": len(all_zips), "error": f"HTTP {exc.code}: {detail}"})

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "excel": str(args.excel),
        "start_date": args.start_date,
        "end_date": args.end_date,
        "results": results,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_json.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "district",
                "zip_count",
                "start_date",
                "end_date",
                "capacity",
                "available",
                "ratio",
                "error",
            ],
        )
        writer.writeheader()
        for item in results:
            writer.writerow(
                {
                    "district": item.get("district"),
                    "zip_count": item.get("zip_count"),
                    "start_date": item.get("start_date"),
                    "end_date": item.get("end_date"),
                    "capacity": item.get("capacity"),
                    "available": item.get("available"),
                    "ratio": item.get("ratio"),
                    "error": item.get("error"),
                }
            )

    with args.output_monthly_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["district", "zip_count", "month", "capacity", "available", "ratio"],
        )
        writer.writeheader()
        for item in results:
            if item.get("error"):
                continue
            for month_row in item.get("monthly_details", []):
                writer.writerow(
                    {
                        "district": item.get("district"),
                        "zip_count": item.get("zip_count"),
                        "month": month_row.get("month"),
                        "capacity": month_row.get("capacity"),
                        "available": month_row.get("available"),
                        "ratio": month_row.get("ratio"),
                    }
                )

    print(f"Wrote {args.output_json}")
    print(f"Wrote {args.output_csv}")
    print(f"Wrote {args.output_monthly_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
