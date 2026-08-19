---
name: ifp-frequency-cap-validation
description: Run IFP inventory forecast API calls with varying frequency caps (DAY, HOUR, MINUTE) and validate avail/capacity ratios against reference expectations. Use when testing frequency caps, IFP forecasts, avail/capacity ratio validation, or RYM frequency cap tests.
---

# IFP Frequency Cap Validation

## API

- **Endpoint:** `POST http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast`
- **Headers:** `Accept: application/json`, `Content-Type: application/json`, `Source: RYM Frequency Cap Test`
- **Requires:** Hulu VPN / internal network access from the caller machine

## What varies for frequency cap tests

Only change fields under `frequency-cap-detail.frequency-caps[0]`:

| Field | Type | Values |
|-------|------|--------|
| `limit` | int | Max impressions in the window (e.g. `2`) |
| `duration` | int | Window length (e.g. `1`, `30`) |
| `duration-unit` | string | `DAY`, `HOUR`, or `MINUTE` only (no `MONTH`) |

Monthly caps use `DAY` with a longer duration (e.g. 4 per 30 days):

```json
{ "limit": 4, "duration": 30, "duration-unit": "DAY" }
```

Example cap variants:

```json
{ "limit": 2, "duration": 1, "duration-unit": "DAY" }
{ "limit": 1, "duration": 1, "duration-unit": "HOUR" }
{ "limit": 3, "duration": 30, "duration-unit": "MINUTE" }
```

Keep `frequency-cap-detail.tier`, dates, ad-products, and targeting constant unless the test matrix requires otherwise.

## Project files

| File | Purpose |
|------|---------|
| `config/base-request.json` | Shared request body; scripts inject the cap per case |
| `reference/cap-ratio-expectations.json` | Test matrix: caps + expected `avail/capacity` ratios |
| `scripts/run_forecasts.py` | Runs all cases, writes `output/results.json` |
| `scripts/validate_results.py` | Compares actual vs expected ratios |

## Workflow

1. Fill in `expected_avail_capacity_ratio` for each case in `reference/cap-ratio-expectations.json`.
2. Run forecasts (on VPN):

**PowerShell (Windows, no Python required):**

```powershell
.\scripts\run-forecasts.ps1
.\scripts\validate-results.ps1
```

**Python (if installed):**

```bash
python scripts/run_forecasts.py
python scripts/validate_results.py
```

Optional: run a single case with `-CaseId 2-per-1-day` (PowerShell) or `--case-id 2-per-1-day` (Python).

## Validation rule

For each successful response:

```
actual_ratio = availability / capacity
```

Pass when `abs(actual_ratio - expected_ratio) <= tolerance` (default `0.001` from reference file).

If response field names differ, update `response_fields` in the reference file and the ratio logic in `scripts/run_forecasts.py`.

## Adding new cases

Append to `reference/cap-ratio-expectations.json`:

```json
{
  "id": "unique-slug",
  "description": "human-readable label",
  "frequency_cap": {
    "limit": 2,
    "duration": 1,
    "duration-unit": "DAY"
  },
  "expected_avail_capacity_ratio": 0.123456,
  "tolerance": 0.001
}
```

## Environment overrides

- `IFP_API_URL` — override API endpoint
- `IFP_SOURCE_HEADER` — override `Source` header value

Never hardcode credentials in scripts or config. This API uses internal network access via the `Source` header.
