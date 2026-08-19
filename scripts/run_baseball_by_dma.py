#!/usr/bin/env python3
"""Run ESPN baseball forecast (sport UUID) for every DMA, 7/16-7/17."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DMA_FILE = ROOT / "reference" / "dma-codes.json"
OUTPUT = ROOT / "output" / "baseball-by-dma-2026-07-16-17.json"
CSV_OUTPUT = ROOT / "output" / "baseball-by-dma-2026-07-16-17.csv"

API_URL = "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast"
SOURCE = "RYM Frequency Cap Test"
SPORT_UUID = "A6C80B78-6176-4ADC-8A4B-D11AC81461E4"
START_DATE = "2026-07-16"
END_DATE = "2026-07-17"


def build_request(dma_code: str) -> dict:
    return {
        "start-date": START_DATE,
        "end-date": END_DATE,
        "ad-products": ["VIDEO"],
        "frequency-cap-detail": {
            "frequency-caps": [{"limit": 2, "duration": 1, "duration-unit": "HOUR"}],
            "tier": "GUARANTEED",
        },
        "targeting-detail": {
            "targeting-rules": [
                {
                    "definition": {
                        "sub-class": "com.disney.digital.ads.rule.manager.common.And",
                        "not": False,
                        "term-list": [
                            {
                                "sub-class": "com.disney.digital.ads.rule.manager.common.Include",
                                "dimension": "publisher",
                                "value-set": ["ESPN"],
                                "not": False,
                            },
                            {
                                "sub-class": "com.disney.digital.ads.rule.manager.common.Include",
                                "dimension": "sport",
                                "value-set": [SPORT_UUID],
                                "not": False,
                            },
                            {
                                "sub-class": "com.disney.digital.ads.rule.manager.common.Include",
                                "dimension": "dma-code",
                                "value-set": [dma_code],
                                "not": False,
                            },
                        ],
                    }
                }
            ]
        },
    }


def post_forecast(body: dict) -> dict:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Source": SOURCE,
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def ratio(capacity: int | float, available: int | float) -> float | None:
    if not capacity:
        return None
    return round(float(available) / float(capacity), 6)


def daily_map(payload: dict) -> dict[str, dict]:
    return {
        row["date"]: {
            "capacity": row.get("capacity", 0),
            "available": row.get("available", 0),
            "ratio": ratio(row.get("capacity", 0), row.get("available", 0)),
        }
        for row in payload.get("daily-details", [])
    }


def main() -> int:
    dma_data = json.loads(DMA_FILE.read_text(encoding="utf-8"))
    by_code: dict[str, str] = dma_data["by_code"]

    results = []
    errors = []

    total = len(by_code)
    for index, (dma_code, dma_name) in enumerate(sorted(by_code.items(), key=lambda x: int(x[0])), start=1):
        print(f"[{index}/{total}] {dma_name} ({dma_code})", flush=True)
        try:
            payload = post_forecast(build_request(dma_code))
            summary = payload.get("summary", {})
            cap = summary.get("capacity", 0)
            avail = summary.get("available", 0)
            results.append(
                {
                    "dma_code": dma_code,
                    "dma_name": dma_name,
                    "capacity": cap,
                    "available": avail,
                    "ratio": ratio(cap, avail),
                    "daily": daily_map(payload),
                }
            )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            errors.append({"dma_code": dma_code, "dma_name": dma_name, "error": detail})
        except Exception as exc:  # noqa: BLE001
            errors.append({"dma_code": dma_code, "dma_name": dma_name, "error": str(exc)})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output_payload = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "dates": f"{START_DATE} to {END_DATE}",
        "publisher": "ESPN",
        "sport_uuid": SPORT_UUID,
        "frequency_cap": "2 per 1 HOUR",
        "dma_count": len(results),
        "totals": {
            "capacity": sum(item["capacity"] for item in results),
            "available": sum(item["available"] for item in results),
        },
        "results": results,
        "errors": errors,
    }
    OUTPUT.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")

    csv_lines = [
        "dma_code,dma_name,date,capacity,available,ratio",
    ]
    for item in results:
        for date, day in item["daily"].items():
            csv_lines.append(
                f"{item['dma_code']},{json.dumps(item['dma_name'])},{date},"
                f"{day['capacity']},{day['available']},{day['ratio'] if day['ratio'] is not None else ''}"
            )
    CSV_OUTPUT.write_text("\n".join(csv_lines) + "\n", encoding="utf-8")

    print(f"\nWrote {OUTPUT}")
    print(f"Wrote {CSV_OUTPUT}")
    print(
        f"Totals: capacity={output_payload['totals']['capacity']:,} "
        f"available={output_payload['totals']['available']:,} "
        f"errors={len(errors)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
