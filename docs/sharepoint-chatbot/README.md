# SharePoint Q&A Chatbot — Implementation Pack

Everything needed to deploy the **ET Anthropic Help Bot** for your team in Microsoft Teams.

## Start here

| Step | Document | Who |
|------|----------|-----|
| 0 | [enterprise-ai-how-to-guide.md](../enterprise-ai-how-to-guide.md) | Everyone — Claude, Copilot, HTML, email, Studio |
| 1 | [it-request-template.md](./it-request-template.md) | You → IT |
| 2 | [copilot-studio-setup-guide.md](./copilot-studio-setup-guide.md) | Bot builder |
| 3 | [teams-deployment-guide.md](./teams-deployment-guide.md) | Bot builder |
| 4 | [team-quick-start.md](./team-quick-start.md) | Share with team |

## Config files (copy into Copilot Studio)

| File | Purpose |
|------|---------|
| [config/agent-system-instructions.txt](./config/agent-system-instructions.txt) | Agent system prompt |
| [config/knowledge-sources.json](./config/knowledge-sources.json) | Approved SharePoint folders |
| [config/sample-topics.json](./config/sample-topics.json) | Test prompts and topic ideas |

## Training deck

Section 10 of the Cursor training PowerPoint includes Copilot Studio walkthrough slides. Regenerate with:

```powershell
cd C:\Users\syeda012\projects\rym-work\ifp-frequency-cap-tests
py scripts\modify_training_pptx.py
```

## Developer-only: SharePoint in Cursor

For **personal** SharePoint search while coding (not a team bot), see [../../scripts/sharepoint-mcp/README.md](../../scripts/sharepoint-mcp/README.md).

## Architecture

```
Team → Teams → Copilot Studio Agent → Microsoft Graph → SharePoint (ET Anthropic)
```

Cursor is not used for the team bot; it is optional for developers via the SharePoint MCP server.
