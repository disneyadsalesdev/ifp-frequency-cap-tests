# IT Request — SharePoint Q&A Bot (Copilot Studio)

Copy the email below and send to your IT / AI enablement contact. Replace bracketed placeholders before sending.

---

**Subject:** Request: Copilot Studio access + SharePoint permissions for ET Anthropic Q&A bot

Hi [IT contact / AI Champions team],

We would like to deploy a **team SharePoint Q&A chatbot** for the ET Anthropic group so teammates can ask questions about training docs, templates, and folder locations in Teams — without hunting through SharePoint manually.

Please confirm or provision the following:

### 1. Licenses

- [ ] **Microsoft Copilot Studio** — builder license for [your name / power users]
- [ ] **Microsoft 365 Copilot** (optional) — for ad-hoc SharePoint Q&A in browser/Teams
- [ ] **Power Platform environment** — production or approved dev environment for the agent

### 2. SharePoint scope

- **Site:** `https://twdc.sharepoint.com/sites/ETAnthropic`
- **Libraries/folders to index (read-only for the bot):**
  - [ ] Shared Documents / Training
  - [ ] Shared Documents / Templates
  - [ ] Site Pages (if applicable)
  - [ ] Other: _______________

We will **not** index tenant-wide content — only approved folders on this site.

### 3. Access & governance

- [ ] Confirm this aligns with **enterprise AI acceptable-use policy** (Claude/Copilot guidelines)
- [ ] Approve **Entra ID group** for bot users: `[Suggested: ET-Anthropic-AI-Bot-Users]`
- [ ] Confirm no restricted data (PII, credentials, unreleased financials) in indexed libraries
- [ ] Security review contact (if required): _______________

### 4. Teams deployment

- [ ] Permission to **publish a Copilot Studio agent** to Teams team: `[Team name]`, channel: `[e.g. #ai-training]`
- [ ] Copilot Studio **Dataverse** connection to SharePoint (if required by tenant policy)

### 5. Timeline

- Target go-live: _______________
- Bot owner / maintainer: [Your name, email]

### Reference

We are following an internal setup guide at `docs/sharepoint-chatbot/copilot-studio-setup-guide.md` in the IFP frequency-cap-tests repo. Happy to walk through the agent design on a quick call.

Thank you,  
[Your name]

---

## IT checklist (for your records)

| Item | Status | Notes |
|------|--------|-------|
| Copilot Studio license assigned | ☐ | |
| M365 Copilot (optional) | ☐ | |
| SharePoint site read access for agent | ☐ | |
| Approved folder list documented | ☐ | |
| Entra group for bot users created | ☐ | |
| Teams channel identified | ☐ | |
| Security / AI policy sign-off | ☐ | |
