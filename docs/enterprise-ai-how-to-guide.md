# Enterprise AI How-To Guide

Step-by-step instructions for Claude, Microsoft Copilot, and Copilot Studio SharePoint bots. Matches **Section 10** of the Cursor training deck.

---

## 1. How to download & access the Claude AI portal

1. Open your company **IT portal** or AI enablement page (ask your manager for the Claude request link).
2. Submit an access request for **Claude Enterprise** — include your team name and use case.
3. Wait for manager and IT approval.
4. When approved, open the **enterprise URL** from IT — do not use consumer `claude.ai` unless IT explicitly allows it.
5. Sign in with **company SSO** (Microsoft Entra) — same credentials as email and SharePoint.
6. Bookmark the portal for daily use.
7. Install the desktop app **only if** IT lists it as an approved method.

---

## 2. How to integrate Claude with PowerPoint & Excel

### Excel

1. Select your table in Excel, or **File → Save As → CSV**.
2. Copy the data and paste it into Claude (remove confidential columns first).
3. Ask Claude, for example:
   - *"Summarize this data in 5 bullet points."*
   - *"Flag any rows where revenue dropped more than 10% week over week."*
   - *"Suggest a pivot table layout for this data."*
4. Copy Claude's output into a new Excel sheet or into PowerPoint.
5. **Verify all numbers and formulas** against the source — do not trust AI totals blindly.

### PowerPoint

1. Paste your slide outline or rough bullets into Claude.
2. Ask, for example:
   - *"Turn this into 8 slides with titles, 3 bullets each, and speaker notes — professional tone."*
3. Copy titles and bullets into your deck.
4. If you have **Microsoft 365 Copilot**: open PowerPoint → click the **Copilot** icon → ask in-app (no copy/paste needed).

### When to use which tool

| Task | Use |
|------|-----|
| Quick edit inside Excel/PowerPoint | Microsoft Copilot (in-app) |
| Deep analysis, long documents, cross-tool reasoning | Claude (browser) |

---

## 3. How to use Claude to create HTML (instead of Excel)

Use HTML when you want a **shareable visual report** that doesn't need Excel formulas.

1. Copy your data from Excel (CSV) or paste a table into Claude.
2. Use a prompt like:

   ```
   Create a self-contained HTML page with:
   - A styled table of this data
   - A simple bar chart (CSS or inline SVG)
   - Embedded CSS, responsive layout, print-friendly styling
   - Single .html file, no external dependencies
   ```

3. Copy Claude's HTML output.
4. Save as `ReportName.html` on your computer.
5. Double-click to open in a browser — verify every number against the source.
6. Share via an approved internal site or email a link.

**When to stay in Excel:** downstream teams need formulas, pivot tables, or data refresh.

---

## 4. How to use Claude to fill out email reports

1. Gather inputs: weekly metrics, bullet notes, or meeting summary (follow data privacy policy).
2. Paste into Claude with a prompt like:

   ```
   Draft a professional weekly status email:
   - Subject line
   - Sections: Wins, Blockers, Next week
   - Audience: [leadership / my team]
   - Tone: professional, under 200 words
   ```

3. Review **every name, date, metric, and attachment reference** before sending.
4. For recurring reports, save the prompt as a template in SharePoint.
5. **Outlook + Copilot:** in compose window, click **Draft with Copilot** for in-place drafting.

---

## 5. How to set up Copilot agents (Teams, SharePoint, M365)

### Prerequisites

Ask IT: *"Do I have Microsoft 365 Copilot and/or Copilot Studio?"*

### Teams

1. Open Teams (desktop or web).
2. Open a chat or channel → click the **Copilot** icon.
3. Try: *"Summarize this channel from the last 7 days"* or *"Draft a reply to the last message."*

### SharePoint

1. Open your site in browser (e.g. `https://twdc.sharepoint.com/sites/ETAnthropic`).
2. Open the **Copilot** pane (where licensed).
3. Ask about pages and documents on that site: *"What's on this site about Cursor training?"*

### Custom agents (Copilot Studio)

For a dedicated team bot, continue to [Section 6](#6-how-to-build-an-ask-bot-in-copilot-studio-sharepoint-qa) and the full guide at [sharepoint-chatbot/copilot-studio-setup-guide.md](./sharepoint-chatbot/copilot-studio-setup-guide.md).

---

## 6. How to build an ask-bot in Copilot Studio (SharePoint Q&A)

Build a Teams bot that answers questions and points to SharePoint folders.

### Step 1 — IT approval

Send [sharepoint-chatbot/it-request-template.md](./sharepoint-chatbot/it-request-template.md) to IT. You need:

- Copilot Studio license
- Approved SharePoint folders to index
- Teams channel for deployment

### Step 2 — Create the agent

1. Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) → sign in with SSO.
2. **Create → New agent** → name it (e.g. *ET Anthropic Help Bot*).
3. Open **Settings → Instructions** and paste text from [config/agent-system-instructions.txt](./sharepoint-chatbot/config/agent-system-instructions.txt).
4. Enable **generative answers**; require **Entra ID sign-in**.

### Step 3 — Connect SharePoint knowledge

1. **Knowledge → Add knowledge → SharePoint**.
2. Select `https://twdc.sharepoint.com/sites/ETAnthropic`.
3. Choose specific folders: **Training**, **Templates**, **AI Guides** — not the entire tenant.
4. Wait 15–60 minutes for indexing.

### Step 4 — Test

Use the Test pane with prompts from [config/sample-topics.json](./sharepoint-chatbot/config/sample-topics.json):

- *"Where is the Cursor training guide?"*
- *"How do I get Claude portal access?"*
- *"Which folder has the IFP templates?"*

The bot should cite real files or say it doesn't know — never invent paths.

### Step 5 — Publish to Teams

1. Click **Publish** in Copilot Studio.
2. **Channels → Microsoft Teams → On**.
3. In Teams: **Apps →** search your agent → **Add to team** → pick channel.
4. Share [team-quick-start.md](./sharepoint-chatbot/team-quick-start.md) in the channel.

Full deployment details: [teams-deployment-guide.md](./sharepoint-chatbot/teams-deployment-guide.md).

---

## Quick reference

| I need to… | Start here |
|------------|------------|
| Get Claude access | Section 1 |
| Use Claude with Excel/PowerPoint | Section 2 |
| Build HTML report instead of Excel | Section 3 |
| Draft email reports | Section 4 |
| Use Copilot in Teams/SharePoint | Section 5 |
| Build SharePoint Q&A bot | Section 6 |

Regenerate training slides after edits:

```powershell
cd C:\Users\syeda012\projects\rym-work\ifp-frequency-cap-tests
py scripts\modify_training_pptx.py
```

Output: `Cursor_Training_Guide_8.11_updated.pptx` in Downloads.
