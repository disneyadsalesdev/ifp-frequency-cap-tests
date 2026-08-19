# Complete IFP + MCP Setup Guide (Every Step Explained)

> **New user?** Open **`docs/NEW-USER-SIMPLE-GUIDE.pdf`** (plain English). Trainers edit `docs/source/NEW-USER-SIMPLE-GUIDE.md` and run `py docs/build_simple_guide_pdf.py`.

This guide explains **everything** for a new user: what MCP is, where each file goes, what each JSON file does, and how to send an IFP forecast API call from Cursor.

---

## Table of contents

1. [Big picture — what talks to what](#1-big-picture--what-talks-to-what)
2. [Words you need (JSON, MCP, API)](#2-words-you-need-json-mcp-api)
3. [What you need before you start](#3-what-you-need-before-you-start)
4. [Folder layout on your computer](#4-folder-layout-on-your-computer)
5. [Every JSON file explained](#5-every-json-file-explained)
6. [Get the MCP server (step by step)](#6-get-the-mcp-server-step-by-step)
7. [Where to save MCP settings (`mcp.json`)](#7-where-to-save-mcp-settings-mcpjson)
8. [Connect Cursor to MCP](#8-connect-cursor-to-mcp)
9. [Send your first API call (3 ways)](#9-send-your-first-api-call-3-ways)
10. [IFP portal — when and how to use it](#10-ifp-portal--when-and-how-to-use-it)
11. [How to update targeting, DMA, product ID](#11-how-to-update-targeting-dma-product-id)
12. [Checklists](#12-checklists)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Big picture — what talks to what

You are **not** automating clicks in the IFP website. You are calling the **same backend API** the website uses.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  YOUR COMPUTER (VPN on)                                                  │
│                                                                          │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │ Cursor chat │───▶│ ifp-mcp-server  │───▶│ IFP Forecast API        │ │
│  │  (Agent)    │    │  server.py      │    │  (POST JSON)            │ │
│  └─────────────┘    └────────▲────────┘    └─────────────────────────┘ │
│                              │ reads                                      │
│                              │                                            │
│                    ifp-frequency-cap-tests/                              │
│                      config/base-request.json                            │
│                      reference/*.json                                    │
│                                                                          │
│  ┌─────────────┐                                                         │
│  │ Browser     │  IFP Portal (optional — for SSO + copying requests)    │
│  └─────────────┘                                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

| Piece | What it is |
|-------|------------|
| **IFP Portal** | Website: https://ifp-portal-prod.aor.prod.hulu.com/home |
| **IFP API** | `http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast` |
| **MCP server** | Small Python program Cursor starts; gives Cursor “tools” to call the API |
| **JSON files** | Text files that store settings, codes, and test cases (not programs) |
| **Scripts** | `.ps1` or `.py` files that run tests without chat |

---

## 2. Words you need (JSON, MCP, API)

### JSON

- A **text file format** for structured data (labels and values).
- Extension: `.json`
- You **edit** it to change dates, targeting, DMA codes in the request template.
- You **do not run** JSON like a program.

Example:

```json
{
  "start-date": "2026-07-08",
  "product-id": 10710
}
```

### API call

- Your computer sends an **HTTP POST** with a **JSON body** to the IFP forecast URL.
- The API responds with JSON (capacity, available, daily breakdown).

### MCP (Model Context Protocol)

- A standard way for **Cursor** to talk to **external tools**.
- **MCP server** = a program on your machine that registers tools like `run_forecast`.
- Cursor starts it using instructions in **`mcp.json`**.

You do **not** open the MCP server in a browser. Cursor runs it in the background when MCP is enabled.

---

## 3. What you need before you start

| Requirement | Why |
|-------------|-----|
| **Hulu VPN** | API and portal are on internal network |
| **Cursor** installed | https://cursor.com |
| **Python 3** | For MCP server only; on Windows use command **`py`** |
| **Two project folders** | See next section |
| **IFP portal access** | SSO login — to verify access and copy request bodies |
| **No API password** for IFP | Uses VPN + `Source` header (team value) |

---

## 4. Folder layout on your computer

Put both projects under something like `C:\Users\<YourName>\projects\`:

```
C:\Users\<YourName>\projects\
│
├── ifp-frequency-cap-tests\          ← TEAM CONFIG + DATA (use git)
│   ├── config\
│   │   └── base-request.json         ← Main forecast request template
│   ├── reference\
│   │   ├── dma-codes.json            ← DMA name ↔ code lookup
│   │   └── cap-ratio-expectations.json ← Frequency cap test list
│   ├── scripts\
│   │   ├── run-forecasts.ps1         ← Run API calls (PowerShell)
│   │   └── validate-results.ps1
│   ├── output\                       ← Results after runs (created automatically)
│   └── docs\                         ← Guides (including this file)
│
└── ifp-mcp-server\                   ← MCP PROGRAM (use git)
    ├── server.py                     ← The MCP server Cursor runs
    └── requirements.txt              ← Python package list (mcp)
```

**Separate from projects — on your user profile:**

```
C:\Users\<YourName>\.cursor\
└── mcp.json                          ← Tells Cursor how to start ifp-mcp-server
```

This file is **per person** (paths use your username). Do not commit secrets here; IFP block has no passwords.

---

## 5. Every JSON file explained

### `config/base-request.json` — **THE REQUEST YOU SEND**

This is the **full forecast request** the API expects (template).

| Section | What it stores |
|---------|----------------|
| `start-date` / `end-date` | Forecast window |
| `ad-products` | e.g. `["VIDEO"]` |
| `frequency-cap-detail` | Cap (limit, duration, MINUTE/HOUR/DAY), **tier**, **product-id** |
| `targeting-detail` | All targeting rules (publisher, country, **dma-code**, MLB rules, etc.) |

**Who edits it:** Team when product, DMA defaults, or targeting changes (often after copying from portal DevTools).

**Used by:** MCP server, `run-forecasts.ps1`, `run_forecasts.py`.

---

### `reference/dma-codes.json` — **LOOKUP ONLY**

Does **not** get sent as a whole file to the API.

| Section | Purpose |
|---------|---------|
| `by_code` | `"803"` → `"Los Angeles"` |
| `by_name` | `"Zanesville"` → `"596"` |

**In the API** you only send:

```json
{
  "dimension": "dma-code",
  "value-set": ["803"]
}
```

Portal shows **names**; API uses **codes**. Use this file to translate.

**Who edits it:** Rarely — run `scripts/build_dma_codes.py` to refresh Nielsen list; add one-off fixes if IFP differs.

---

### `reference/cap-ratio-expectations.json` — **TEST MATRIX**

List of frequency cap scenarios for automated testing.

Each **case** has:

- `id` — short name, e.g. `2-per-1-day`
- `frequency_cap` — limit, duration, duration-unit
- `expected_avail_capacity_ratio` — number for PASS/FAIL (or `null` to skip validation)

**Used by:** `run-forecasts.ps1` / MCP `run_cap_test_matrix` and `validate_cap_test_matrix`.

---

### `output/results.json` — **GENERATED OUTPUT**

Created **after** you run tests. Contains API responses. Safe to delete/regenerate.

Other outputs (e.g. `output/baseball-by-dma-*.json`) are from custom scripts.

---

### `~/.cursor/mcp.json` — **CURSOR SETTINGS (NOT IN REPO)**

Tells Cursor:

- **Where** `server.py` lives
- **Which** test project folder to read (`IFP_TESTS_ROOT`)
- **API URL** and **Source** header

Example IFP block only:

```json
{
  "mcpServers": {
    "ifp-forecast": {
      "type": "stdio",
      "command": "py",
      "args": [
        "C:/Users/YourName/projects/ifp-mcp-server/server.py"
      ],
      "env": {
        "IFP_API_URL": "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast",
        "IFP_SOURCE_HEADER": "RYM Frequency Cap Test",
        "IFP_TESTS_ROOT": "C:/Users/YourName/projects/ifp-frequency-cap-tests"
      }
    }
  }
}
```

If you already have other servers (e.g. Snowflake), **merge** `"ifp-forecast"` into existing `"mcpServers"` — do not delete other entries unless you mean to.

**Path rules on Windows:** Use forward slashes `/` in `mcp.json` even on Windows.

---

## 6. Get the MCP server (step by step)

### Step 6.1 — Get the code

Copy or clone **`ifp-mcp-server`** from your team (git, zip, shared drive).

You must have this file:

`ifp-mcp-server/server.py`

### Step 6.2 — Install Python package

Open **PowerShell** or **Terminal**:

```powershell
py -m pip install -r C:\Users\YourName\projects\ifp-mcp-server\requirements.txt
```

That installs the **`mcp`** library (one time per machine).

### Step 6.3 — Quick test (optional)

```powershell
py C:\Users\YourName\projects\ifp-mcp-server\server.py
```

It may look like it “hangs” — that is normal (waiting for Cursor). Press Ctrl+C to stop. Cursor will start it automatically when configured.

---

## 7. Where to save MCP settings (`mcp.json`)

| OS | Full path |
|----|-----------|
| **Windows** | `C:\Users\<YourName>\.cursor\mcp.json` |
| **Mac** | `/Users/<YourName>/.cursor/mcp.json` |

**How to create:**

1. Open File Explorer → go to `C:\Users\<YourName>\`
2. Show hidden folders if needed — folder **`.cursor`** may be hidden
3. Create folder `.cursor` if missing
4. Create file `mcp.json` with the IFP block from [section 5](#mcpjson)
5. Replace `YourName` in all three paths

Also get **`ifp-frequency-cap-tests`** on the same machine — MCP reads JSON from `IFP_TESTS_ROOT`.

---

## 8. Connect Cursor to MCP

1. **Save** `mcp.json`
2. **Quit Cursor completely** and reopen (or **Command Palette → Reload Window**)
3. Open **Cursor Settings → MCP**
4. Find **`ifp-forecast`**
   - **Green** = connected
   - **Red** = click logs; usually wrong path or missing `pip install mcp`
5. Connect **VPN**
6. In Cursor: **File → Open Folder** → open **`ifp-frequency-cap-tests`**
7. Open chat (**Ctrl+I**), choose **Agent** mode

---

## 9. Send your first API call (3 ways)

### Way A — MCP in chat (recommended after setup)

Examples:

```
Use ifp_server_info to show configuration.
```

```
Run a forecast: 2 per 1 HOUR from 2026-07-08 to 2026-07-08 using the base request.
```

```
Run the full frequency cap test matrix.
```

Cursor calls MCP tools → MCP loads `base-request.json` → POST to API → shows capacity/available.

### Way B — PowerShell script (no MCP)

```powershell
cd C:\Users\YourName\projects\ifp-frequency-cap-tests
.\scripts\run-forecasts.ps1
```

Reads same JSON files; writes `output/results.json`.

### Way C — IFP portal (manual)

Open portal URL, build forecast, submit — for comparison only; not automated.

---

## 10. IFP portal — when and how to use it

**URL:** https://ifp-portal-prod.aor.prod.hulu.com/home

| Use portal for… | Use API/MCP for… |
|-----------------|------------------|
| Login / SSO check | Batch forecasts, cap tests, Cursor chat |
| Pick product ID (targeting auto-fills in UI) | Repeatable runs from saved JSON |
| Copy correct API payload | Validation scripts |

### Copy a request from DevTools

1. VPN on → open portal → start forecast
2. **F12** → **Network** tab → filter **Fetch/XHR**
3. Find request to **`forecast`** (or inventory forecast path)
4. **Copy request payload** (JSON)
5. Paste into **`config/base-request.json`** (clean up — remove `"supported": true` if those are response-only fields)
6. Save → run MCP or script again

**Important:** Product ID in the portal fills targeting **in the browser only**. The API does **not** build that targeting from `product-id` alone. Your saved `base-request.json` must include the full `targeting-detail`.

---

## 11. How to update targeting, DMA, product ID

| Change | Edit this | Notes |
|--------|-----------|--------|
| **Dates** | `base-request.json` → `start-date`, `end-date` | Or pass dates in MCP `run_forecast` |
| **Product** | `frequency-cap-detail` → `product-id`, `tier` | e.g. `10710`, `SPONSORSHIP` |
| **Frequency cap (default in template)** | `frequency-cap-detail` → `frequency-caps` | Test matrix overrides per case in `cap-ratio-expectations.json` |
| **Publishers, country, MLB rules, etc.** | `targeting-detail` → `term-list` | Best copied from portal DevTools |
| **DMA in template** | Add/update term with `"dimension": "dma-code"` | Values like `"803"` — lookup names in `dma-codes.json` |
| **Multiple DMAs** | `"value-set": ["803", "501"]` | Same dimension, multiple codes |
| **One-off DMA in MCP** | Pass `dma=["803"]` to tool | MCP adds/overrides `dma-code` term |
| **Expected test ratios** | `cap-ratio-expectations.json` | For validate script |

### Product ID reminder

```json
"frequency-cap-detail": {
  "frequency-caps": [ { "limit": 2, "duration": 1, "duration-unit": "HOUR" } ],
  "tier": "SPONSORSHIP",
  "product-id": 10710
}
```

`product-id` is a **number**, inside `frequency-cap-detail` — not a top-level string label.

---

## 12. Checklists

### New user — setup

- [ ] VPN works
- [ ] Portal login works
- [ ] Cloned `ifp-frequency-cap-tests` and `ifp-mcp-server`
- [ ] `py -m pip install -r ...\requirements.txt`
- [ ] Created `C:\Users\<You>\.cursor\mcp.json` with correct paths
- [ ] Restarted Cursor — MCP **ifp-forecast** is green
- [ ] Opened `ifp-frequency-cap-tests` folder in Cursor
- [ ] First successful forecast (chat or `run-forecasts.ps1`)

### Trainer — explain these files

- [ ] `base-request.json` = what we POST
- [ ] `dma-codes.json` = lookup only
- [ ] `cap-ratio-expectations.json` = cap tests
- [ ] `mcp.json` = personal Cursor config
- [ ] `output/` = results

---

## 13. Troubleshooting

| Problem | What to do |
|---------|------------|
| MCP red / not starting | Fix paths in `mcp.json`; run `py -m pip install mcp`; read MCP logs in Settings |
| `Python was not found` | Use **`py`** not `python` on Windows |
| Network error | Turn on VPN |
| 400 Unsupported targeting | Wrong dimension; use **`dma-code`** not `dma`; compare with portal payload |
| Capacity huge vs portal | Missing targeting in `base-request.json` |
| Scripts disabled | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |
| Chat does not use MCP | VPN on, MCP green, Agent mode, ask to use `run_forecast` or `ifp_server_info` |

---

## Quick reference card

| Item | Value |
|------|--------|
| Portal | https://ifp-portal-prod.aor.prod.hulu.com/home |
| API | `POST http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast` |
| MCP config | `C:\Users\<You>\.cursor\mcp.json` |
| MCP server file | `...\ifp-mcp-server\server.py` |
| Request template | `...\ifp-frequency-cap-tests\config\base-request.json` |
| DMA lookup | `...\reference\dma-codes.json` |
| Cap tests | `...\reference\cap-ratio-expectations.json` |
| Source header | `RYM Frequency Cap Test` (team default) |

---

*Internal use — IFP MCP onboarding. Share this file + both project folders + IFP block for `mcp.json`.*
