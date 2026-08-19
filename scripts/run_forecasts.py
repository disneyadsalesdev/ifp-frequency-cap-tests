#!/usr/bin/env python3
"""Run IFP inventory forecast API calls for each cap case in the reference file."""

from __future__ import annotations

import argparse
import copy
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def apply_frequency_cap(body: dict[str, Any], cap: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(body)
    payload["frequency-cap-detail"]["frequency-caps"] = [cap]
    return payload


def post_forecast(
    api_url: str,
    source: str,
    body: dict[str, Any],
    timeout_seconds: int,
) -> dict[str, Any]:
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

    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def compute_ratio(response: dict[str, Any]) -> float | None:
    availability = response.get("availability")
    capacity = response.get("capacity")
    if availability is None or capacity is None:
        return None
    if capacity == 0:
        return None
    return float(availability) / float(capacity)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run IFP frequency cap forecast matrix")
    parser.add_argument(
        "--base-request",
        type=Path,
        default=Path("config/base-request.json"),
        help="Base forecast request body",
    )
    parser.add_argument(
        "--expectations",
        type=Path,
        default=Path("reference/cap-ratio-expectations.json"),
        help="Reference file with cap cases and expected ratios",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/results.json"),
        help="Where to write combined run results",
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("IFP_API_URL", DEFAULT_API_URL),
        help="Forecast API endpoint (override with IFP_API_URL env var)",
    )
    parser.add_argument(
        "--source",
        default=os.getenv("IFP_SOURCE_HEADER", DEFAULT_SOURCE),
        help="Value for the Source request header",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="HTTP timeout in seconds",
    )
    parser.add_argument(
        "--case-id",
        action="append",
        dest="case_ids",
        help="Run only specific case id(s); repeatable",
    )
    args = parser.parse_args()

    base_request = load_json(args.base_request)
    expectations = load_json(args.expectations)
    cases = expectations.get("cases", [])

    if args.case_ids:
        selected = {case_id for case_id in args.case_ids}
        cases = [case for case in cases if case.get("id") in selected]
        if not cases:
            print("No matching cases found for --case-id", file=sys.stderr)
            return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for case in cases:
        case_id = case.get("id", "unknown")
        cap = case["frequency_cap"]
        payload = apply_frequency_cap(base_request, cap)

        entry: dict[str, Any] = {
            "case_id": case_id,
            "description": case.get("description"),
            "frequency_cap": cap,
            "expected_avail_capacity_ratio": case.get("expected_avail_capacity_ratio"),
            "request": payload,
            "ran_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            response = post_forecast(
                api_url=args.api_url,
                source=args.source,
                body=payload,
                timeout_seconds=args.timeout,
            )
            entry["response"] = response
            entry["actual_avail_capacity_ratio"] = compute_ratio(response)
            entry["status"] = "ok"
        except urllib.error.HTTPError as exc:
            entry["status"] = "http_error"
            entry["http_status"] = exc.code
            entry["error"] = exc.read().decode("utf-8", errors="replace")
        except urllib.error.URLError as exc:
            entry["status"] = "network_error"
            entry["error"] = str(exc.reason)
        except json.JSONDecodeError as exc:
            entry["status"] = "invalid_json_response"
            entry["error"] = str(exc)

        results.append(entry)
        print(f"{case_id}: {entry['status']}")

    output = {
        "api_url": args.api_url,
        "source_header": args.source,
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }

    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
