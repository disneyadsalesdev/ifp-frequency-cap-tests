#!/usr/bin/env python3
"""Run IFP forecasts for each individual zip code from an Excel file."""

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
            {"month": month, "capacity": capacity, "available": available, "ratio": ratio}
        )
    return monthly


def apply_postal_code(body: dict[str, Any], postal_code: str) -> dict[str, Any]:
    payload = copy.deepcopy(body)
    term_list = payload["targeting-detail"]["targeting-rules"][0]["definition"]["term-list"]
    term_list[:] = [term for term in term_list if term.get("dimension") != "postal-code"]
    term_list.append(
        {
            "sub-class": INCLUDE,
            "dimension": "postal-code",
            "value-set": [postal_code],
            "not": False,
            "supported": True,
        }
    )
    return payload


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


def load_completed_keys(checkpoint: Path) -> set[tuple[str, str]]:
    if not checkpoint.exists():
        return set()
    completed: set[tuple[str, str]] = set()
    with checkpoint.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            completed.add((row["district"], row["zip_code"]))
    return completed


def append_checkpoint(checkpoint: Path, row: dict[str, Any]) -> None:
    with checkpoint.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def zip_rows_from_excel(df) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for district in df.columns:
        for value in df[district].dropna():
            rows.append({"district": district, "zip_code": str(int(value)).zfill(5)})
    return rows


def write_outputs(
    rows: list[dict[str, Any]],
    output_json: Path,
    output_monthly_csv: Path,
    output_summary_csv: Path,
    excel: Path,
    start_date: str,
    end_date: str,
) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    for row in rows:
        if row.get("error"):
            summary_rows.append(
                {
                    "district": row["district"],
                    "zip_code": row["zip_code"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "capacity": None,
                    "available": None,
                    "ratio": None,
                    "error": row["error"],
                }
            )
            continue
        summary_rows.append(
            {
                "district": row["district"],
                "zip_code": row["zip_code"],
                "start_date": start_date,
                "end_date": end_date,
                "capacity": row["capacity"],
                "available": row["available"],
                "ratio": row["ratio"],
                "error": "",
            }
        )
        for month_row in row.get("monthly_details", []):
            monthly_rows.append(
                {
                    "district": row["district"],
                    "zip_code": row["zip_code"],
                    "month": month_row["month"],
                    "capacity": month_row["capacity"],
                    "available": month_row["available"],
                    "ratio": month_row["ratio"],
                }
            )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "excel": str(excel),
        "start_date": start_date,
        "end_date": end_date,
        "zip_count": len(rows),
        "results": rows,
    }
    with output_json.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    with output_summary_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "district",
                "zip_code",
                "start_date",
                "end_date",
                "capacity",
                "available",
                "ratio",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    with output_monthly_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["district", "zip_code", "month", "capacity", "available", "ratio"],
        )
        writer.writeheader()
        writer.writerows(monthly_rows)


def write_wide_excel(monthly_csv: Path, output_excel: Path) -> None:
    import pandas as pd

    monthly = pd.read_csv(monthly_csv)
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        for metric in ["available", "capacity", "ratio"]:
            wide = monthly.pivot_table(
                index="month",
                columns="zip_code",
                values=metric,
                aggfunc="first",
            ).sort_index()
            wide.index.name = "month"
            wide.to_excel(writer, sheet_name=metric)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run IFP forecasts for each zip code")
    parser.add_argument("--excel", type=Path, required=True)
    parser.add_argument("--base-request", type=Path, default=Path("config/base-request.json"))
    parser.add_argument("--start-date", default="2026-08-10")
    parser.add_argument("--end-date", default="2026-12-31")
    parser.add_argument("--checkpoint", type=Path, default=Path("output/gmmb-by-zip-checkpoint.jsonl"))
    parser.add_argument("--output-json", type=Path, default=Path("output/gmmb-by-zip-forecasts.json"))
    parser.add_argument(
        "--output-summary-csv",
        type=Path,
        default=Path("output/gmmb-by-zip-forecasts-summary.csv"),
    )
    parser.add_argument(
        "--output-monthly-csv",
        type=Path,
        default=Path("output/gmmb-by-zip-forecasts-monthly.csv"),
    )
    parser.add_argument(
        "--output-wide-excel",
        type=Path,
        default=Path("output/gmmb-by-zip-forecasts-monthly-wide.xlsx"),
    )
    parser.add_argument("--api-url", default=os.getenv("IFP_API_URL", DEFAULT_API_URL))
    parser.add_argument("--source", default=os.getenv("IFP_SOURCE_HEADER", DEFAULT_SOURCE))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--limit", type=int, default=0, help="Run only first N pending zips (0 = all)")
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("pandas and openpyxl are required: py -m pip install pandas openpyxl", file=sys.stderr)
        return 1

    base_request = load_json(args.base_request)
    df = pd.read_excel(args.excel)
    zip_rows = zip_rows_from_excel(df)
    completed = load_completed_keys(args.checkpoint)
    pending = [row for row in zip_rows if (row["district"], row["zip_code"]) not in completed]

    if args.limit:
        pending = pending[: args.limit]

    print(
        f"Total zips: {len(zip_rows)} | completed: {len(completed)} | pending: {len(pending)}",
        flush=True,
    )

    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(pending, start=1):
        district = item["district"]
        zip_code = item["zip_code"]
        print(f"[{index}/{len(pending)}] {district} {zip_code}", flush=True)
        body = apply_postal_code(base_request, zip_code)
        body["start-date"] = args.start_date
        body["end-date"] = args.end_date
        try:
            response = post_forecast(args.api_url, args.source, body, args.timeout)
            summary = response["summary"]
            capacity = summary["capacity"]
            available = summary["available"]
            ratio = None if not capacity else round(float(available) / float(capacity), 6)
            row = {
                "district": district,
                "zip_code": zip_code,
                "start_date": args.start_date,
                "end_date": args.end_date,
                "capacity": capacity,
                "available": available,
                "ratio": ratio,
                "monthly_details": aggregate_monthly(response.get("daily-details", [])),
            }
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            row = {
                "district": district,
                "zip_code": zip_code,
                "error": f"HTTP {exc.code}: {detail}",
            }
        except urllib.error.URLError as exc:
            row = {"district": district, "zip_code": zip_code, "error": str(exc)}

        append_checkpoint(args.checkpoint, row)

    all_rows: list[dict[str, Any]] = []
    with args.checkpoint.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                all_rows.append(json.loads(line))

    write_outputs(
        all_rows,
        args.output_json,
        args.output_monthly_csv,
        args.output_summary_csv,
        args.excel,
        args.start_date,
        args.end_date,
    )
    write_wide_excel(args.output_monthly_csv, args.output_wide_excel)

    errors = sum(1 for row in all_rows if row.get("error"))
    print(f"Wrote {args.output_summary_csv}")
    print(f"Wrote {args.output_monthly_csv}")
    print(f"Wrote {args.output_wide_excel}")
    print(f"Done: {len(all_rows)} zips, {errors} errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
