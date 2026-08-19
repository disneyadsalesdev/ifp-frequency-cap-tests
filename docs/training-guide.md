# Cursor Training Guide

**New users:** open **`docs/NEW-USER-SIMPLE-GUIDE.pdf`**. This file is extra detail for later.

---

## Table of contents

1. [Install Cursor](#install-cursor)
2. [New hire: startup prompts & settings](#new-hire-startup-prompts--settings)
3. [Cursor Settings (step by step)](#cursor-settings-step-by-step)
4. [Agent, models & run modes (Run / Allow / Always)](#agent-models--run-modes-run--allow--always)
5. [Day-to-day tools (IFP, daily report, Snowflake)](#day-to-day-tools-ifp-daily-report-snowflake)
6. [IFP portal & DevTools — targeting exercise](#ifp-portal--devtools--targeting-exercise)
7. [Mission Control & weekly MSTR pulls](#mission-control--weekly-mstr-pulls)
8. [Dashboards & producing outputs](#dashboards--producing-outputs)
9. [The three chat workflows](#the-three-chat-workflows)
10. [Copy-paste prompts](#copy-paste-prompts)
11. [Common problems](#common-problems)
12. [Security](#security)

**Before IFP API work:** Connect to **Hulu VPN**.

---

## Install Cursor

1. Open **[https://cursor.com](https://cursor.com)** in your browser.
2. Click **Download** → choose **Windows** (or Mac).
3. Run the installer (`.exe` on Windows). Use default options unless IT says otherwise.
4. Open **Cursor** from the Start menu.
5. **Sign in** when prompted (work account / SSO if your team requires it).
6. Optional: **Help → Check for Updates** so you match the team’s Cursor version.

You do **not** need Cursor to read JSON in Notepad — but you need it for Agent chat, MCP, and running team scripts from the editor.

---

## New hire: startup prompts & settings

Do this **once** on your first day, in order.

### A. Projects on disk

```text
C:\Users\<YourName>\projects\
├── ifp-frequency-cap-tests\    ← IFP JSON, scripts, docs
├── ifp-mcp-server\             ← server.py (MCP)
└── all-publishers-daily-report\  ← only if you own the daily report
```

Full MCP setup: **[complete-ifp-mcp-setup-guide.md](./complete-ifp-mcp-setup-guide.md)**.

### B. One-time commands (PowerShell)

```powershell
py --version
py -m pip install -r C:\Users\<YourName>\projects\ifp-mcp-server\requirements.txt
```

### C. Cursor first open

1. **File → Open Folder** → `ifp-frequency-cap-tests`
2. **`Ctrl+I`** → open chat
3. At the top of chat, choose **Agent** (when you want actions) or **Ask** (questions only)
4. **Settings → MCP** → confirm **`ifp-forecast`** is **green** (VPN not required for green status; required for live forecast)

### D. First prompts (safe — no VPN for 1–4)

**Ask mode:**

```
Explain @reference/cap-ratio-expectations.json in simple terms.
What is one test case?
```

```
Using @reference/dma-codes.json, what is the DMA code for Baton Rouge?
```

```
Explain @config/base-request.json: dates, product-id, and main targeting.
Do not change any files.
```

**Agent mode:**

```
Create practice-notes.md with 4 bullets summarizing caps, DMA codes, and base-request.json.
```

**Agent + VPN on (optional):**

```
Use ifp_server_info to show configuration.
Run a forecast for 2026-07-08, 2 per 1 HOUR, using the base request.
Show summary capacity and available.
```

### E. Run mode for new hires

Until you are comfortable: set **Settings → Agents → Run Mode** so **shell and MCP tools ask you before they run**. See [Run modes](#agent-models--run-modes-run--allow--always) below. Do **not** use “run everything” on day one.

---

## Cursor Settings (step by step)

| Step | Action |
|------|--------|
| 1 | Open Cursor |
| 2 | Click **gear** (bottom-left) **or** press **`Ctrl+,`** |
| 3 | Use the **search box** at the top of settings |

| Search for | Why |
|------------|-----|
| **MCP** | List servers; green/red status; view logs for `ifp-forecast` |
| **Agents** / **Approvals** / **Run Mode** | Control when terminal & MCP run without asking |
| **Keyboard Shortcuts** | Confirm **Ctrl+I** (chat), **Ctrl+`** (terminal) |
| **Models** | Default model for chat (if your org allows changes) |

**Edit MCP without the UI:** open `C:\Users\<You>\.cursor\mcp.json` in any editor → save → **Ctrl+Shift+P** → **Developer: Reload Window**.

**Open personal config folder:** File Explorer → `C:\Users\<You>\.cursor\` (enable **Hidden items** if needed).

---

## Agent, models & run modes (Run / Allow / Always)

### Start a new chat / pick a mode

1. **`Ctrl+I`** opens the chat panel.
2. At the top of the panel:
   - **Mode:** **Ask** | **Agent** | **Plan** (labels may vary slightly by version)
   - **Model:** dropdown — use team default unless told otherwise
3. **New chat:** click **+** or “New Chat” in the chat panel so old context does not confuse IFP runs.

| Mode | Use when |
|------|----------|
| **Ask** | Learning, explaining JSON, no file changes |
| **Agent** | Run forecasts, run scripts, edit config |
| **Plan** | Large multi-file changes — review the plan first |

### When Cursor wants to run something

Applies to **terminal commands**, **MCP tools** (e.g. `run_forecast`), and sometimes **Fetch**.

You may see buttons like:

| Button / choice | Meaning |
|-----------------|--------|
| **Run** (or **Approve**) | Run this action once |
| **Skip** / **Reject** | Do not run |
| **Add to allowlist** | Trust this command or MCP tool for later (use carefully) |

**Settings → Agents → Approvals & Execution → Run Mode** (Cursor 3.6+):

| Run mode | Behavior (summary) |
|----------|---------------------|
| **Allowlist** | Only allowlisted actions run silently; others prompt |
| **Auto-review** | Allowlist + sandbox + AI review — fewer prompts (common default on new installs) |
| **Run everything** | No prompts — **not recommended** for new hires |

**Team recommendation for onboarding:** use a mode that **prompts** for shell and MCP until you trust the workflow. Docs: [cursor.com/docs/agent/security/run-modes](https://cursor.com/docs/agent/security/run-modes).

**MCP specifically:** when the agent calls `run_forecast`, read the tool name in the approval card. Approve only if VPN is on and the request matches what you asked.

### File edits (diffs)

Separate from Run/Allow: Agent shows **Accept** / **Reject** on file changes. Always read red/green diffs before Accept — especially `config/base-request.json`.

---

## Day-to-day tools (IFP, daily report, Snowflake)

| Job | Open folder | VPN | Typical prompt / action |
|-----|-------------|-----|-------------------------|
| **IFP forecast** | `ifp-frequency-cap-tests` | **Yes** | Agent: *Run a forecast for …* or MCP tools |
| **Cap test matrix** | same | **Yes** | *Run the frequency cap test matrix* or `.\scripts\run-forecasts.ps1` |
| **Update targeting** | same | For test call | Edit `config/base-request.json` (often from portal DevTools) |
| **Daily publishers report** | `all-publishers-daily-report` | No* | *Run @dailypublisherscript.py`* |
| **Snowflake SQL (if configured)** | any + MCP | Per org | MCP **Snowflake** tools — never paste PAT in chat |

\*Daily report needs **Outlook** and today’s **MSTR email**, not IFP VPN.

**Weekly rhythm (example):**

| Day | Task |
|-----|------|
| Daily | MSTR emails arrive → daily report script → review Outlook draft → send |
| As needed | IFP forecasts for deals / caps (VPN + Cursor or scripts) |
| Weekly | Review Mission Control subscriptions; refresh dashboards if filters changed |

---

## IFP portal & DevTools — targeting exercise

Use this lab to build a correct **`config/base-request.json`** (portal fills targeting in the UI; the API needs the full JSON).

**URL:** https://ifp-portal-prod.aor.prod.hulu.com/home  
**Requires:** Hulu VPN + SSO.

### Exercise steps

1. **VPN on** → open portal → log in.
2. Start a **new forecast** (same product/workflow your team uses — e.g. sponsorship product).
3. In the UI, set:
   - Date range  
   - **Product** (note **product-id**, e.g. `10710`)  
   - **Targeting** (publishers, country, DMA, etc.)  
   - **Frequency cap** (e.g. 2 per HOUR)  
4. Open **Developer Tools:**
   - **Windows:** **`F12`** or **`Ctrl+Shift+I`**
   - **Mac:** **`Cmd+Option+I`**
5. Go to the **Network** tab.
6. Enable **Preserve log** (checkbox) so requests are not cleared on navigation.
7. Filter: **Fetch/XHR** (hide static assets).
8. In the portal, click **Run** / **Submit** on the forecast so the API fires.
9. In the Network list, find a request whose path contains **`forecast`** or **`inventory/forecast`**.
10. Click that row → **Payload** / **Request** tab (Chrome) or **Request** body (Edge/Firefox).
11. **Copy** the JSON request body (not the response).
12. Paste into **`config/base-request.json`** in the repo (replace or merge carefully).
13. **Clean up:** remove fields that are clearly response-only if you pasted the wrong tab; keep `targeting-detail`, `frequency-cap-detail`, dates, `ad-products`.
14. Save → VPN on → test in Cursor: *Run a forecast using base-request for [same date]* and compare capacity/available to the portal.

### What to verify in the copied JSON

| Field | Check |
|-------|--------|
| `frequency-cap-detail` | `product-id`, `tier`, `frequency-caps` |
| `targeting-detail` | `term-list` includes real rules (not empty if portal showed targeting) |
| DMA | dimension **`dma-code`**, values as strings e.g. `"803"` |
| Dates | `start-date`, `end-date` match your exercise |

**Lookup:** DMA names → codes in `reference/dma-codes.json`.

---

## Mission Control & weekly MSTR pulls

**Mission Control** (MicroStrategy) is where teams **schedule** reports and manage **subscriptions** — separate from Cursor. Your daily report script consumes **Excel attachments from email** that often originate from MSTR schedules.

> **Internal URL:** Ask your manager or analytics lead for **MicroStrategy Library** and **Mission Control** links for Disney/Hulu. Paste the canonical URL into this doc when the team agrees on one.

### Typical weekly / scheduled pull setup

1. **VPN / network** per your org (same as other internal analytics tools).
2. Open **MicroStrategy Library** (web) → sign in with SSO.
3. Find the report or dashboard (e.g. **All Publisher Daily Report**).
4. Open **Mission Control** (from Library menu or direct URL — team-specific).
5. **Create subscription** or **schedule:**
   - Recurrence: **Daily** or **Weekly** (match when emails must arrive before your script).
   - Format: **Excel** if the daily report script expects `.xlsx`.
   - Delivery: **Email** to your team list (sender often appears as MicroStrategy, e.g. `microstrategy-prod@dpdo.info`).
6. Save → confirm a test run arrives in Outlook.
7. **Day-of workflow:** when email arrives, run **`dailypublisherscript.py`** (or ask Cursor: *Run @dailypublisherscript.py*).

### If email is late

- Check Mission Control job history (failed run).
- Confirm subscription still active and date filters rolled forward.
- Ask Cursor: *"Why did dailypublisherscript fail to find today's MSTR email?"*

---

## Dashboards & producing outputs

| Output | How it is produced |
|--------|---------------------|
| **Daily email + Excel attachment** | MSTR schedule → Outlook → `dailypublisherscript.py` → master template + pivots → draft email |
| **IFP capacity / available** | MCP or `run-forecasts.ps1` → chat or `output/results.json` |
| **Cap test PASS/FAIL** | `validate-results.ps1` or MCP `validate_cap_test_matrix` |
| **Ad-hoc analysis in Cursor** | Agent + `@` files; export CSV from script output; paste tables into slides (redact sensitive data) |
| **Live MSTR dashboard** | Library in browser — filters, export, or subscribe via Mission Control |

**Producing a dashboard for a meeting:**

1. Run or refresh the underlying report (MSTR or IFP).
2. Export to Excel/CSV if needed.
3. Use master template pivots (daily report) or summarize in Cursor: *"Summarize output/results.json as a table of cap vs ratio."*
4. Copy into PowerPoint/Sheets — follow team data-handling rules.

---

## The three chat workflows

### Daily publishers report

```
Run @dailypublisherscript.py
```

Manual: `cd ...\all-publishers-daily-report` → `py dailypublisherscript.py`  
Use **`py`** not `python` on Windows if you see “Python was not found.”

### IFP forecasts

```
Run a forecast for [date] Hulu US, [city] DMA, [N] per [hour/day]
```

```
Run the frequency cap test matrix
```

PowerShell: `cd ...\ifp-frequency-cap-tests` → `.\scripts\run-forecasts.ps1`

Cap units: `MINUTE`, `HOUR`, `DAY` only.

### Ask for help

| Task | Prompt |
|------|--------|
| DMA code | *What's the DMA code for [city]?* |
| Change targeting | *Add Disney Plus to publisher targeting in base-request* |
| Explain | *Explain @dailypublisherscript.py step by step* |

---

## Copy-paste prompts

```
Run @dailypublisherscript.py

Run a forecast for 2026-07-08 Hulu US, Baton Rouge, 2 per hour

Run the frequency cap test matrix

What's the DMA code for Baton Rouge?

Use ifp_server_info to show configuration.

Walk me through copying IFP targeting from DevTools into base-request.json
```

---

## Common problems

| Problem | What to do |
|---------|------------|
| `Python was not found` | Use **`py`** |
| IFP connection error | Hulu VPN |
| MCP red | Fix `mcp.json` paths; `py -m pip install mcp`; Reload Window |
| Unexpected command ran | Settings → Agents → stricter Run Mode |
| MSTR email missing | Mission Control schedule / Outlook |
| Portal vs API numbers differ | Missing `targeting-detail` in `base-request.json` — redo DevTools exercise |
| PowerShell blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

---

## Security

- Do not paste passwords, PATs, or tokens into chat.
- Do not share your full `mcp.json` if it contains Snowflake or other secrets.
- Review diffs before Accept; do not auto-send email (script opens draft by default).

---

## Shortcuts

| Action | Key |
|--------|-----|
| Open chat | `Ctrl+I` |
| Open terminal | `` Ctrl+` `` |
| Command palette | `Ctrl+Shift+P` |
| Settings | `Ctrl+,` |

---

**Slides:** `py docs/build_deck.py` → `docs/training-guide.pptx` (includes table of contents slide).
