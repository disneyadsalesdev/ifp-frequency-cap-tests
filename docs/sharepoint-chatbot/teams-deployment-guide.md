# Teams Deployment — ET Anthropic Help Bot

After building the agent in [copilot-studio-setup-guide.md](./copilot-studio-setup-guide.md).

---

## Step 1 — Publish the agent

1. Copilot Studio → open **ET Anthropic Help Bot**
2. Click **Publish** → confirm environment
3. Wait for "Published successfully"

---

## Step 2 — Enable Microsoft Teams channel

1. **Channels** (left nav) → **Microsoft Teams**
2. Turn **On** the Teams channel
3. Choose availability:
   - **Show to users in my org** — recommended start
   - Or restrict to specific **Entra ID group** (from IT request)

---

## Step 3 — Install to a team

**Option A — Team app (recommended for a dedicated channel)**

1. Teams → **Apps** → search for your agent name (**ET Anthropic Help Bot**)
2. **Add to a team** → select team (e.g. ET Anthropic / AI Training)
3. Choose channel (e.g. **General** or **#ai-training**)
4. Pin the channel tab if your team uses it daily

**Option B — Personal app**

1. Users open **Copilot** / **Agents** in Teams
2. Find **ET Anthropic Help Bot** under **Built for your org**
3. Pin for quick access

---

## Step 4 — Announce to the team

Post this in the channel (customize links):

```
📢 ET Anthropic Help Bot is live

Ask questions about training docs, templates, and SharePoint folders — in this channel or by @mentioning the bot.

Try:
• "Where is the Cursor training guide?"
• "How do I get Claude portal access?"
• "What's the MSTR daily report process?"
• "Which folder has the IFP templates?"

The bot answers from approved SharePoint content only. If it can't find something, ask in this channel or check the site home.

Quick start: [attach team-quick-start.md or PDF]
```

Share [team-quick-start.md](./team-quick-start.md) as a channel file or OneNote page.

---

## Step 5 — Pin example prompts

Create a **Teams Wiki** or **SharePoint list** with saved prompts your team reuses. Link from the channel description.

---

## Access control checklist

- [ ] Only ET Anthropic (or approved) members in the Teams team
- [ ] Entra group matches IT approval
- [ ] Bot not published tenant-wide unless intended
- [ ] Channel moderators know escalation path for wrong answers

---

## Updating the bot

1. Edit agent in Copilot Studio
2. **Publish** again
3. Teams users get updates automatically (may take a few minutes)
4. Post a short "what's new" note if knowledge sources changed significantly

---

## Fallback: M365 Copilot only

If Copilot Studio is not approved, teammates with **M365 Copilot** licenses can:

1. Open `https://twdc.sharepoint.com/sites/ETAnthropic` in browser
2. Open the **Copilot** pane
3. Ask questions about pages/files on that site

Limitation: no custom branding, no dedicated Teams bot, no folder-navigation instructions unless documented on the site.
