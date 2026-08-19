# IFP Portal & MCP Setup (Teammate Guide)

Share this with anyone setting up Cursor to work with **Inventory Forecast Portal (IFP)** and the **IFP forecast API**.

---

## 1. IFP Portal (website)

| Item | Value |
|------|--------|
| **Production portal URL** | https://ifp-portal-prod.aor.prod.hulu.com/home |
| **Network** | **Hulu VPN / corporate network** required |
| **Login** | Company SSO (same as other internal Disney/Hulu tools) |

**What the portal is for:** Building forecasts in the UI, picking product ID, DMA, frequency cap, etc.

**What scripts/MCP use:** The **forecast API** directly (see below). You do **not** need the portal open for automated runs, but you **do** need VPN.

---

## 2. IFP Forecast API (what Cursor/scripts call)

| Item | Value |
|------|--------|
| **Endpoint** | `POST http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast` |
| **Headers** | `Accept: application/json`, `Content-Type: application/json`, `Source: RYM Frequency Cap Test` (or team-agreed value) |
| **Auth** | Internal network access (VPN); no browser login on the API itself |

**Important:** The portal auto-fills targeting when you enter a **product ID**. The API does **not** generate that targeting for you—you must send the full request body (copy from DevTools after a portal run, or use the team’s `base-request.json`).

---

## 3. Test project (frequency cap / O1 / DMA)

| Item | Path (example) |
|------|----------------|
| **Repo / folder** | `ifp-frequency-cap-tests` |
| **Base request template** | `config/base-request.json` |
| **Cap test matrix** | `reference/cap-ratio-expectations.json` |
| **DMA name ↔ code** | `reference/dma-codes.json` (Nielsen codes; validated vs IFP) |
| **Run tests (PowerShell)** | `scripts/run-forecasts.ps1`, `scripts/validate-results.ps1` |
| **Docs** | `docs/colleague-writeup.md`, `docs/cursor-guide.md` |

**Prerequisites:** VPN, Python (`py` on Windows) or PowerShell only for scripts.

---

## 4. MCP server setup in Cursor

MCP lets Cursor call IFP tools from chat (run forecast, cap matrix, etc.).

### 4.1 IFP MCP server code

| Item | Location |
|------|----------|
| **Server** | `ifp-mcp-server/server.py` |
| **Dependencies** | `pip install -r ifp-mcp-server/requirements.txt` (package: `mcp`) |

### 4.2 Cursor config file

Create or edit **`%USERPROFILE%\.cursor\mcp.json`** (Windows) or **`~/.cursor/mcp.json`** (Mac/Linux).

**Template** — replace paths with your machine’s paths:

```json
{
  "mcpServers": {
    "ifp-forecast": {
      "type": "stdio",
      "command": "py",
      "args": [
        "C:/YOUR_USERNAME/projects/ifp-mcp-server/server.py"
      ],
      "env": {
        "IFP_API_URL": "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast",
        "IFP_SOURCE_HEADER": "RYM Frequency Cap Test",
        "IFP_TESTS_ROOT": "C:/YOUR_USERNAME/projects/ifp-frequency-cap-tests"
      }
    }
  }
}
```

**Notes:**

- Use **`py`** on Windows if `python` opens the Microsoft Store stub.
- Use **forward slashes** in paths in `mcp.json` on Windows.
- Do **not** commit secrets to git; IFP uses VPN + `Source` header, not API keys in this setup.

### 4.3 Verify MCP

1. **Restart Cursor** (or Reload Window).
2. **Settings → MCP** → server **`ifp-forecast`** should be **green**.
3. In chat (on VPN): ask to use **`ifp_server_info`** or run a forecast via MCP tools.

### 4.4 MCP tools (IFP)

| Tool | Purpose |
|------|---------|
| `run_forecast` | Single forecast (cap, dates, optional DMA codes) |
| `run_cap_test_matrix` | All cases in `cap-ratio-expectations.json` |
| `validate_cap_test_matrix` | PASS/FAIL vs expected ratios |
| `ifp_server_info` | Show API URL, paths, config |

**DMA in API:** dimension **`dma-code`**, values like `"803"` (portal shows names; see `reference/dma-codes.json`).

**O1 product:** `"product-id": 10710` inside **`frequency-cap-detail`**, tier often **`SPONSORSHIP`**, plus portal targeting in `targeting-detail`.

---

## 5. Quick checklist for a new teammate

| Step | Action |
|------|--------|
| 1 | Install [Cursor](https://cursor.com) |
| 2 | Connect **VPN** |
| 3 | Clone/copy **`ifp-frequency-cap-tests`** and **`ifp-mcp-server`** |
| 4 | `py -m pip install -r ifp-mcp-server/requirements.txt` |
| 5 | Edit **`~/.cursor/mcp.json`** with local paths |
| 6 | Restart Cursor → check **Settings → MCP** |
| 7 | Open IFP portal URL to confirm SSO + UI access |
| 8 | Optional: run `.\scripts\run-forecasts.ps1` from test project |

---

## 6. Getting correct API payloads from the portal

1. Open https://ifp-portal-prod.aor.prod.hulu.com/home  
2. **F12 → Network → Fetch/XHR**  
3. Run a forecast in the UI  
4. Copy the **`forecast`** POST body → update `config/base-request.json`  

Use this when changing **product ID**, **DMA**, or targeting—the API will not infer portal targeting from product ID alone.

---

## 7. Contacts / internal resources

- Update this section with your team’s Slack channel, Confluence page, or on-call if applicable.

---

*Internal use — IFP / inventory forecasting · update paths per machine*
