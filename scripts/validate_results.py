#!/usr/bin/env python3
"""Validate IFP forecast results against expected avail/capacity ratios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def ratio_matches(actual: float, expected: float, tolerance: float) -> bool:
    return abs(actual - expected) <= tolerance


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate IFP forecast ratio results")
    parser.add_argument(
        "--results",
        type=Path,
        default=Path("output/results.json"),
        help="Results file produced by run_forecasts.py",
    )
    parser.add_argument(
        "--expectations",
        type=Path,
        default=Path("reference/cap-ratio-expectations.json"),
        help="Reference file with expected ratios",
    )
    args = parser.parse_args()

    results_doc = load_json(args.results)
    expectations = load_json(args.expectations)
    default_tolerance = float(expectations.get("default_tolerance", 0.001))

    expected_by_id = {
        case["id"]: case for case in expectations.get("cases", []) if case.get("id")
    }

    failures = 0
    for result in results_doc.get("results", []):
        case_id = result.get("case_id", "unknown")
        expected_case = expected_by_id.get(case_id, {})
        expected_ratio = expected_case.get("expected_avail_capacity_ratio")
        tolerance = float(expected_case.get("tolerance", default_tolerance))
        actual_ratio = result.get("actual_avail_capacity_ratio")
        status = result.get("status")

        if status != "ok":
            print(f"FAIL {case_id}: forecast call failed ({status})")
            failures += 1
            continue

        if expected_ratio is None:
            print(f"SKIP {case_id}: no expected ratio configured")
            continue

        if actual_ratio is None:
            print(f"FAIL {case_id}: could not compute avail/capacity ratio from response")
            failures += 1
            continue

        if ratio_matches(actual_ratio, expected_ratio, tolerance):
            print(f"PASS {case_id}: ratio {actual_ratio:.6f} ~= {expected_ratio:.6f}")
        else:
            print(
                f"FAIL {case_id}: ratio {actual_ratio:.6f} != {expected_ratio:.6f} "
                f"(tolerance {tolerance})"
            )
            failures += 1

    if failures:
        print(f"\n{failures} failure(s)")
        return 1

    print("\nAll configured cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
