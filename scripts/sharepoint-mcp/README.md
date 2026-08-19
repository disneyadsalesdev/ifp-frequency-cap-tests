# SharePoint MCP Server (Developer-Only)

Read-only SharePoint search for **Cursor** while coding. This is **not** the team Teams chatbot — use [Copilot Studio](../../docs/sharepoint-chatbot/README.md) for that.

## What it does

| Tool | Description |
|------|-------------|
| `search_sharepoint` | Search drive items and pages you can access |
| `get_site_info` | Metadata for ET Anthropic (or another) site |
| `list_site_drives` | List document libraries on a site |

## Prerequisites

1. **Azure app registration** (IT or personal dev app in tenant):
   - Platform: Mobile and desktop applications
   - Redirect URI: `https://login.microsoftonline.com/common/oauth2/nativeclient`
   - API permissions (delegated): `Sites.Read.All`, `User.Read`
   - Admin consent may be required for `Sites.Read.All`

2. Python 3.10+

## Install

```powershell
cd C:\Users\syeda012\projects\rym-work\ifp-frequency-cap-tests\scripts\sharepoint-mcp
py -m pip install -r requirements.txt
```

## Configure Cursor

1. Copy `mcp.json.example` values into your Cursor MCP config (`~/.cursor/mcp.json` or project `.cursor/mcp.json`).
2. Set `AZURE_CLIENT_ID` and `AZURE_TENANT_ID` (Disney tenant ID).
3. Restart Cursor → enable **sharepoint-search** server.

First run opens **device code login** in the terminal — sign in with Disney SSO.

## Example prompts in Cursor

```
Search SharePoint for "Cursor training guide"
List document libraries on the ET Anthropic site
```

## Security

- Read-only delegated permissions (acts as signed-in user).
- Never commit client secrets; public client + device flow only.
- Do not use for PII-heavy libraries without security review.
- Team Q&A should use Copilot Studio, not this MCP server.

## Evaluation summary

| Criterion | Assessment |
|-----------|------------|
| Team chatbot | Use Copilot Studio → Teams (recommended) |
| Personal dev use in Cursor | This MCP server |
| IT approval | App registration + Sites.Read.All consent |
| Maintenance | Low — Graph search API, no SharePoint scraping |
