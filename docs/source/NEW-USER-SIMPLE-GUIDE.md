# Cursor + IFP + MSTR — New User Guide

**Version for new hires — read top to bottom. Do not skip the “Where do I start?” page.**

---

# PAGE 1 — Where do I start? (read this first)

**You only need ONE file today:**

| What | Where |
|------|--------|
| **This guide (PDF)** | `ifp-frequency-cap-tests/docs/NEW-USER-SIMPLE-GUIDE.pdf` |
| **Live training slides (optional)** | Ask trainer for `training-guide.pptx` |

**Ignore other files in `docs/` until you are comfortable.** Your trainer uses hidden source files to rebuild this PDF.

---

## Which part of this guide do I need?

| I need to… | Go to page / section |
|------------|----------------------|
| Install Cursor from scratch | **Part A — Download Cursor** |
| First-day computer setup (folders, Python, MCP) | **Part B — Day 1 setup** |
| Open Cursor Settings, MCP green, Run Mode | **Part C — Cursor Settings** |
| Learn Agent vs Ask, New Chat, Run/Skip buttons | **Part D — Chat & approvals** |
| Copy-paste first exercises in Cursor | **Part E — Startup prompts** |
| Run an IFP forecast every day | **Part F — IFP day to day** |
| Copy targeting from IFP website (F12) | **Part G — IFP DevTools lab** |
| Daily MSTR email + Excel report | **Part H — MSTR day to day** |
| Schedule weekly/daily MSTR emails | **Part I — Mission Control** |
| Something broke | **Part J — Fix it** |

---

## The three jobs (pick yours)

| Job | What you do | VPN? |
|-----|-------------|------|
| **IFP forecast** | Type in Cursor chat → get capacity/available | **Yes** (Hulu VPN) |
| **MSTR daily report** | Cursor runs script → Outlook draft → you Send | No (need Outlook) |
| **Mission Control** | Schedule MSTR emails in browser (setup once) | Per your org |

---

## Day 1 order (check off as you go)

- [ ] Part A — Install Cursor  
- [ ] Part B — Get folders, Python, mcp.json, MCP green  
- [ ] Part C — Settings (MCP + Run Mode)  
- [ ] Part D — Read how Agent and Run buttons work  
- [ ] Part E — Do startup prompts (Ask then Agent)  
- [ ] Part F — One test forecast (VPN on)  
- [ ] Part H — Only if you own the daily report  

---

# PART A — Download Cursor (every click)

You need Cursor **before** anything else.

### A1. Open the website

1. Open **Chrome** or **Edge**.
2. Click the address bar at the top.
3. Type: **cursor.com**
4. Press **Enter**.

### A2. Download

5. On the Cursor home page, click the **Download** button.
6. If it asks **Windows** or **Mac**, choose **Windows**.
7. Wait for the file to download (often in your **Downloads** folder).
8. The file name is usually like **Cursor Setup.exe**.

### A3. Install

9. Open **Downloads** in File Explorer.
10. Double-click **Cursor Setup.exe**.
11. If Windows asks “Do you want to allow this app to make changes?” click **Yes**.
12. Follow the installer (**Next** → **Install** → **Finish**).

### A4. First open

13. Open Cursor from the **Start menu** (search “Cursor”).
14. If it asks you to **Sign in**, sign in (use work account if IT requires it).
15. If it asks about importing VS Code settings, you can click **Skip** or **Continue** — either is fine.
16. Optional: **Help** menu → **Check for Updates**.

### A5. Pin it (optional)

17. With Cursor open, right-click its icon on the taskbar → **Pin to taskbar**.

**Done with Part A.** Continue to Part B.

---

# PART B — Day 1 setup (one time only)

Ask a teammate to sit with you for **B4–B7** if you get stuck.

### B1. Check access

1. Connect **Hulu VPN** — confirm it works.
2. Open **https://ifp-portal-prod.aor.prod.hulu.com/home** — confirm you can log in (SSO).
3. Ask trainer for **git clone URLs** (see `docs/CLONE-INSTRUCTIONS.md`) or zip files if git is not ready yet.

### B2. Create your projects folder

4. Open **File Explorer**.
5. Go to `C:\Users\` and open **your** folder (your Windows name).
6. If there is no **`projects`** folder: right-click → **New** → **Folder** → name it **`projects`**.

### B3. Get two folders on your PC

You must have **both** of these when done:

```
C:\Users\YourName\projects\ifp-frequency-cap-tests
C:\Users\YourName\projects\ifp-mcp-server
```

**Option 1 — Git (trainer gives you URLs):**

7. Press **Windows key**, type **PowerShell**, press **Enter**.
8. Copy/paste (trainer replaces the URLs):

```powershell
cd C:\Users\YourName\projects
git clone https://github.com/disneyadsalesdev/ifp-frequency-cap-tests.git
git clone https://github.com/disneyadsalesdev/ifp-mcp-server.git
```

**Option 2 — Zip files:**

7. Unzip both zips.
8. Move folders so names and paths match exactly above.

| Folder | You use it for… |
|--------|-----------------|
| `ifp-frequency-cap-tests` | **Open this in Cursor every day** for IFP |
| `ifp-mcp-server` | Holds `server.py` — Cursor starts it; you rarely open this folder |

### B4. Install Python (for IFP helper only)

Python **3.10+** is required. **Node.js is NOT required** for this setup. You do **not** need the Python extension in Cursor for MCP.

**Windows**

9. Go to **python.org/downloads** → Download Python 3.x → run the installer.
10. Check **Add python.exe to PATH** on the first screen → **Install Now**.
11. Open **PowerShell**:

```powershell
py --version
py -m pip install -r C:\Users\YourName\projects\ifp-mcp-server\requirements.txt
```

**Mac**

9. Go to **python.org/downloads** → Download macOS installer (.pkg) → run it.  
   *(Or: `brew install python@3.12` if you use Homebrew.)*
10. Open **Terminal**:

```bash
python3 --version
python3 -m pip install -r /Users/YourName/projects/ifp-mcp-server/requirements.txt
```

### B5. Create mcp.json (personal settings file)

This file is **on your PC only** — not in the git folders.

12. File Explorer → `C:\Users\YourName\`
13. **View** → turn on **Hidden items**
14. Open folder **`.cursor`** (create it if missing)
15. Create file **`mcp.json`**
16. Trainer sends you a template — replace **`YourName`** with your username.

**Windows** — `C:\Users\YourName\.cursor\mcp.json` (use `"command": "py"`):

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

**Mac** — `/Users/YourName/.cursor/mcp.json` (use `"command": "python3"`). See also `docs/templates/mcp.mac.json`.

17. **Save** the file.

### B6. Reload Cursor

18. In Cursor: **Ctrl+Shift+P**
19. Type **Reload Window**
20. Press **Enter**

### B7. Open IFP folder in Cursor

21. **File → Open Folder**
22. Select **`ifp-frequency-cap-tests`**
23. Left sidebar should show **`config`**, **`docs`**, **`scripts`**, etc.

**Part B done.** Next: Part C (Settings).

---

# PART C — Cursor Settings (where to click)

### C1. Open Settings

| Step | Action |
|------|--------|
| 1 | Click **gear icon** bottom-left of Cursor **OR** press **Ctrl+,** |
| 2 | A settings panel opens |

### C2. Check MCP (IFP helper connected)

| Step | Action |
|------|--------|
| 3 | In settings search box, type **MCP** |
| 4 | Find server name **`ifp-forecast`** |
| 5 | Status must be **green** |
| 6 | If **red**: click for **logs** → ask trainer (usually wrong path in mcp.json or Part B4 failed) |

### C3. Set Run Mode (Run / Always / Ask — important for new users)

When the Agent runs commands or IFP tools, Cursor may show **Run**, **Skip**, or **Add to allowlist**.

| Step | Action |
|------|--------|
| 7 | In settings search, type **Run Mode** or **Agents** |
| 8 | Open **Agents → Approvals & Execution** (wording may vary) |
| 9 | For **new hires**, choose a mode that **asks before** running things |

| Run Mode (name in Settings) | What it means for you |
|----------------------------|------------------------|
| **Allowlist** (empty list) | Cursor asks before almost every command/MCP action |
| **Auto-review** | Some things run automatically after a review — fewer popups |
| **Run everything** | **Do not use on day 1** — things run without asking |

10. **Trainer tip:** Until you are comfortable, pick the strictest mode your IT allows.

### C4. After any mcp.json edit

11. **Ctrl+Shift+P** → **Reload Window**

**Part C done.**

---

# PART D — Chat, Agent, New Chat, Run buttons

### D1. Open chat

1. Press **Ctrl+I**
2. Chat panel opens (usually on the right)

### D2. Start a NEW chat (do this for each new task)

3. At top of chat panel, click **+** or **New Chat**
4. Why: old messages confuse the Agent

### D3. Pick the mode (top of chat panel)

| Mode | When to use | Can it change files / run IFP? |
|------|-------------|--------------------------------|
| **Ask** | Learning, explaining JSON | **No** — safe for practice |
| **Agent** | Forecasts, scripts, edits | **Yes** — with your approval |
| **Plan** | Big multi-step jobs | Makes a plan first, then Agent runs |

5. **IFP forecast** → use **Agent**
6. **“What does this file mean?”** → use **Ask**

### D4. Pick a model (optional)

7. Dropdown at top of chat — leave **team default** unless IT says otherwise

### D5. When you see approval buttons

**For terminal commands and MCP (IFP) tools:**

| Button | What to do |
|--------|------------|
| **Run** / **Approve** | OK this **one time** — only if VPN is on (for IFP) and request matches what you asked |
| **Skip** / **Reject** | Do not run — ask trainer |
| **Add to allowlist** | Trust for later — **ask trainer before** using |

**For file edits (separate from Run):**

| Button | What to do |
|--------|------------|
| **Accept** | Keep the file change |
| **Reject** | Undo the change |

---

# PART E — Startup prompts (new hire — do in order)

Open **`ifp-frequency-cap-tests`** in Cursor first.

### E1. Ask mode — no VPN needed

1. **Ctrl+I** → **New Chat** → mode **Ask**
2. Paste and send:

```
Explain reference/cap-ratio-expectations.json in simple terms.
What is one test case?
```

3. **New Chat** → **Ask** → paste:

```
What is the DMA code for Baton Rouge? Use reference/dma-codes.json.
```

4. **New Chat** → **Ask** → paste:

```
Explain config/base-request.json — dates and main targeting only.
Do not change any files.
```

### E2. Agent mode — creates one practice file

5. **New Chat** → mode **Agent**
6. Paste:

```
Create practice-notes.md with 4 bullets summarizing caps, DMA codes, and base-request.json.
```

7. Read the diff → **Accept** if OK

### E3. Agent + VPN — one live forecast

8. Turn **Hulu VPN** on
9. **New Chat** → **Agent**
10. Paste:

```
Use ifp_server_info to show configuration.
```

11. If Cursor shows MCP approval → read tool name → **Run**
12. Paste:

```
Run a forecast for July 8, 2026, Hulu US, Baton Rouge, 2 per hour.
Show capacity and available.
```

13. If approval appears again → **Run** (VPN must be on)

**Part E done** — you are set up to use Cursor for IFP.

---

# PART F — IFP day to day (every forecast)

Repeat these steps each time.

| Step | Do this |
|------|---------|
| 1 | **Hulu VPN** on |
| 2 | Cursor → **File → Open Folder** → `ifp-frequency-cap-tests` |
| 3 | **Ctrl+I** → **New Chat** → **Agent** |
| 4 | Type your request in plain English, e.g.: `Run a forecast for [date], Hulu US, [city], [N] per hour. Show capacity and available.` |
| 5 | Click **Run** on any MCP approval if prompted |
| 6 | Read **capacity** and **available** in the reply |

**Cap units:** only **MINUTE**, **HOUR**, or **DAY** (e.g. 4 per 30 DAY for monthly-style caps).

**City names:** portal shows names; API uses **numbers** — ask Cursor or check `reference/dma-codes.json`.

---

# PART G — IFP DevTools lab (targeting exercise)

Use when **numbers don’t match the portal** or **product/targeting changed**.

**Goal:** Copy the exact request the portal sends → save into `config/base-request.json`.

### G1. Portal setup

1. **VPN on**
2. Browser → **https://ifp-portal-prod.aor.prod.hulu.com/home**
3. Log in
4. Build the forecast in the UI exactly like the deal:
   - Dates  
   - Product (note **product-id**)  
   - Targeting (publishers, country, DMA, etc.)  
   - Frequency cap  

### G2. Open Developer Tools

5. Press **F12** on keyboard (or **Ctrl+Shift+I**)
6. A panel opens — usually at bottom or side of browser
7. Click tab **Network**
8. Check box **Preserve log** (keeps requests after page changes)
9. Click filter **Fetch/XHR** (hides images/CSS)

### G3. Capture the request

10. In the portal, click **Run forecast** / **Submit**
11. In Network list, find a row containing **forecast** in the name or URL
12. **Click that row**
13. On the right, open **Payload** or **Request** (Chrome) / **Request** body (Edge)
14. Copy the **JSON request body** — **NOT** the Response tab

### G4. Save into project

15. In Cursor, open **`config/base-request.json`**
16. Replace contents with copied JSON **or** ask Agent:

```
Help me update config/base-request.json with this portal request payload: [paste JSON here]
```

17. **Save** the file
18. **VPN on** → run **Part F** again → compare numbers to portal

**Important:** Picking a product in the portal fills targeting **in the browser only**. The saved JSON must include full **targeting-detail**, not just product-id.

---

# PART H — MSTR day to day (daily publishers report)

**Different job from IFP.** You need folder **`all-publishers-daily-report`**.

| Step | Do this |
|------|---------|
| 1 | Wait for **MicroStrategy email** in Outlook (often from **microstrategy-prod@dpdo.info**) with today’s `.xlsx` attachments |
| 2 | Cursor → **File → Open Folder** → `all-publishers-daily-report` |
| 3 | **Ctrl+I** → **New Chat** → **Agent** |
| 4 | Type: `Run dailypublisherscript.py` |
| 5 | Click **Run** if Cursor asks to run terminal commands |
| 6 | Script updates Excel and opens an **Outlook draft** |
| 7 | **You** review the draft and click **Send** — Cursor does not send email for you |

**If email is missing:** check **Part I (Mission Control)** schedule or ask analytics teammate.

---

# PART I — Mission Control (schedule MSTR emails)

**Mission Control** = MicroStrategy tool to **schedule** report emails. You set this up **once** (or verify existing schedules); it is **not** Cursor.

> **URL:** Ask your manager for **MicroStrategy Library** and **Mission Control** links. Paste team URL here when known: ___________________________

### I1. Find your report in Library

1. Connect VPN/network per org rules
2. Open **MicroStrategy Library** (browser) → SSO login
3. Search **All Publisher Daily Report** (or your team’s report name)
4. Open the report to confirm it looks correct

### I2. Create or edit a subscription in Mission Control

5. Open **Mission Control** (from Library menu or direct link)
6. Click **Create subscription** or **New schedule** (wording varies)
7. Select the report
8. Set **Recurrence:**
   - **Daily** — for daily report script (email must arrive before you run Part H)
   - **Weekly** — for weekly pulls/dashboards
9. Set **Format:** **Excel** (`.xlsx`) if the daily script expects Excel
10. Set **Delivery:** email to your team distribution list
11. **Save**
12. Run a **test** — confirm email arrives in Outlook

### I3. Weekly checklist (example)

| When | Action |
|------|--------|
| Each business day | MSTR email arrived? → Part H daily script |
| Weekly | Mission Control job succeeded? (ask analytics if emails stop) |
| After IFP deal change | Part G DevTools → Part F test forecast |

---

# PART J — Fix it

| Problem | Try this |
|---------|----------|
| Forecast fails / timeout | **VPN on?** |
| MCP red in Settings | Trainer checks `mcp.json` paths + Part B4 pip install + Reload Window |
| “Python was not found” | Use **`py`** not **`python`** |
| Cursor ran something scary | Part C3 — stricter Run Mode; use **Ask** when learning |
| IFP numbers ≠ portal | Part G — missing targeting in `base-request.json` |
| No MSTR email today | Part I — subscription failed or late |
| PowerShell script blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (once) |

**Never paste passwords or tokens in chat.**

---

# PART K — Who to ask

| Question | Ask |
|----------|-----|
| Cursor install, git, mcp.json | Your **trainer** |
| IFP wrong numbers / product | **IFP owner** on team |
| Daily report / Outlook / Excel | **Daily report owner** |
| Mission Control / MSTR schedules | **Analytics** teammate |
| IT / VPN / SSO | **IT help desk** |

---

# Quick reference

| Item | Location |
|------|----------|
| This guide (PDF) | `docs/NEW-USER-SIMPLE-GUIDE.pdf` |
| IFP folder to open in Cursor | `...\ifp-frequency-cap-tests` |
| MCP config | `C:\Users\You\.cursor\mcp.json` |
| IFP portal | https://ifp-portal-prod.aor.prod.hulu.com/home |
| Open chat | **Ctrl+I** |
| Open Settings | **Ctrl+,** |
| Reload Cursor | **Ctrl+Shift+P** → Reload Window |

**End of guide.**
