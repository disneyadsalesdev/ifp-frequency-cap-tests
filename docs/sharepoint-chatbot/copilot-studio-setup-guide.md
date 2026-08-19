# Copilot Studio Setup — ET Anthropic SharePoint Q&A Bot

Step-by-step guide to build the team chatbot. Complete [it-request-template.md](./it-request-template.md) first.

---

## Prerequisites

- Copilot Studio access (https://copilotstudio.microsoft.com) with Disney SSO
- Edit rights on the ET Anthropic SharePoint site (or IT adds knowledge sources for you)
- Approved folder list in [config/knowledge-sources.json](./config/knowledge-sources.json)

---

## Step 1 — Create the agent

1. Open **Copilot Studio** → **Create** → **New agent**.
2. Name: **ET Anthropic Help Bot**
3. Description: *Answers questions about ET Anthropic training docs, templates, and SharePoint folders.*
4. Language: English
5. Save in your team's **Power Platform environment** (IT may specify prod vs dev).

---

## Step 2 — Add instructions (system prompt)

1. Open the agent → **Settings** → **Generative AI** (or **Instructions** / **System message**).
2. Paste the full text from [config/agent-system-instructions.txt](./config/agent-system-instructions.txt).
3. Enable **Generative answers** / **Use generative AI** if prompted.
4. Set **Content moderation** to your org default (do not disable).

---

## Step 3 — Connect SharePoint knowledge

1. Go to **Knowledge** → **Add knowledge** → **SharePoint**.
2. Select site: `https://twdc.sharepoint.com/sites/ETAnthropic`
3. Choose **specific libraries/folders** from [config/knowledge-sources.json](./config/knowledge-sources.json):
   - Shared Documents → Training
   - Shared Documents → Templates
   - (Add others after IT approval)
4. Optionally add **Site pages** for the ET Anthropic home/how-to pages.
5. Wait for indexing to complete (may take 15–60 minutes for large libraries).

**Tip:** Do not add the entire tenant or unrelated sites.

---

## Step 4 — Add topics (optional but recommended)

For predictable answers, add **Topics** in Copilot Studio:

| Topic | Trigger phrases | Response |
|-------|-----------------|----------|
| Greeting | hello, hi, help | Welcome message + 3 example questions |
| Escalate to human | talk to person, IT ticket | Link to #ai-training channel or IT portal |
| Out of scope | password, salary, confidential | Policy reminder + escalate |

Full test phrases: [config/sample-topics.json](./config/sample-topics.json)

---

## Step 5 — Test before publishing

Use the **Test** pane with every prompt in `sample-topics.json` → `testPrompts`:

```
Where is the Q3 forecast template?
How do I get access to the Claude AI portal?
What's the MSTR daily report workflow?
```

**Pass criteria:**
- Answers cite connected SharePoint content or clearly say content is not indexed
- Folder paths are included when relevant
- No hallucinated URLs or file names

Fix gaps by adding missing docs to SharePoint or expanding knowledge sources.

---

## Step 6 — Security settings

1. **Authentication:** Require users to sign in (Entra ID).
2. **Sharing:** Restrict to specific security group (see IT request template).
3. **Analytics:** Enable so you can review unanswered questions monthly.

---

## Step 7 — Publish

1. Click **Publish** (top right).
2. Continue to [teams-deployment-guide.md](./teams-deployment-guide.md) to add the Teams channel.

---

## Maintenance

| When | Action |
|------|--------|
| New training deck uploaded | Re-publish agent (Knowledge may auto-refresh; confirm in test pane) |
| Folder restructure | Update knowledge sources + system instructions paths |
| Monthly | Review Analytics → add topics for frequent unanswered questions |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "I don't have access to SharePoint" in Studio | IT must grant Copilot Studio service account / connector permissions |
| Bot gives wrong file names | Re-index knowledge; add explicit topic with correct path |
| Users can't see bot in Teams | Republish; reinstall app to team; check Entra group membership |
| M365 Copilot works but Studio bot doesn't | Separate products — Studio needs its own SharePoint knowledge connection |
