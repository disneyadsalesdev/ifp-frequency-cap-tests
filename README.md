# IFP Frequency Cap Tests

Team repo for **Cursor + IFP forecast** onboarding and daily use.

## New hires — start here

1. Read **`docs/START-HERE.md`**
2. Follow **`docs/NEW-USER-SIMPLE-GUIDE.pdf`** or **`.pptx`**
3. Clone **`ifp-mcp-server`** (sibling repo) and set up `~/.cursor/mcp.json`

## What’s in this repo

| Path | Purpose |
|------|---------|
| `config/base-request.json` | Forecast request template (update from IFP portal) |
| `reference/dma-codes.json` | City name ↔ DMA code lookup |
| `reference/cap-ratio-expectations.json` | Cap test cases and expected ratios |
| `docs/templates/mcp.json` | Windows MCP config template |
| `docs/templates/mcp.mac.json` | Mac MCP config template |
| `docs/CLONE-INSTRUCTIONS.md` | Git clone steps (Windows + Mac) |

## Clone (with MCP server)

```bash
git clone https://github.com/disneyadsalesdev/ifp-frequency-cap-tests.git
git clone https://github.com/disneyadsalesdev/ifp-mcp-server.git
```

See **`docs/CLONE-INSTRUCTIONS.md`** for pip install and MCP setup.
