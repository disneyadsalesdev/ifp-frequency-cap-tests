# Cursor Anatomy — 3-Minute Recording Script

Use this while recording with Loom, OBS, or Windows Game Bar (`Win + G` → Capture → Record).

**Before you hit Record:** Open Cursor with your RYM Projects workspace, close unrelated tabs, and have `assets/cursor-anatomy-annotated.png` ready to show for the intro (optional).

---

## Prep checklist (2 min)

- [ ] Cursor open, workspace loaded, no sensitive files visible in the tree
- [ ] Agent panel open on the right (empty or fresh chat is fine)
- [ ] Bottom panel visible (Output or Terminal tab — either works)
- [ ] No file open in the editor (Cursor logo empty state is ideal for the tour)
- [ ] Screen recorder ready; mic on if you want voiceover
- [ ] Optional: open `assets/cursor-anatomy-annotated.png` in a tab for the first 10 seconds

---

## Recording script

### 0:00 – 0:15 | Intro

**Show:** Full Cursor window (all four areas visible).

**Say:**
> "This is Cursor — an AI-powered code editor. It has four main areas. I'll walk through each one in about three minutes."

**Do:** Pause on the full layout for 2–3 seconds. Optionally flash the annotated screenshot, then return to Cursor.

---

### 0:15 – 0:55 | File Explorer (red)

**Show:** Left sidebar — activity bar + file tree.

**Say:**
> "On the left is the **File Explorer**. This is your project — folders and files for everything you're working on."

**Do (click in order, slowly):**

1. Point at the **activity bar icons** (far left strip):
   - "The top icon is Explorer — your file tree."
   - Click **Search** — "Search finds text across the whole project."
   - Click back to **Explorer**.
   - Briefly click **Source Control** — "Git lives here."
   - Click back to **Explorer**.

2. Point at the **toolbar on the right of the workspace header** (above the tree):
   - "Up here you can create a new file, new folder, refresh the tree, or collapse all folders."

3. Click a harmless file, e.g. `README.md` or any `.py` in `scripts/`:
   - "Click any file to open it in the editor."

**Keyboard shortcut (optional):** `Ctrl + B` to hide/show sidebar — "You can toggle the sidebar anytime."

---

### 0:55 – 1:25 | Code Editor (green/teal)

**Show:** Center top — the file you just opened (or empty editor if you skipped opening a file).

**Say:**
> "The **Code Editor** is where you read and write code. Each open file gets its own tab."

**Do:**

1. If no file is open, click one from the tree now.
2. Point at the **tab** at the top — "Tabs switch between open files."
3. Make a tiny harmless edit (add a space or comment) — "You edit here like any text editor."
4. `Ctrl + S` — "Save with Control-S."
5. `Ctrl + Z` to undo if you added something — keep the file clean.

**Say:**
> "Syntax highlighting, autocomplete, and inline AI suggestions all appear in this area."

---

### 1:25 – 1:50 | Output / Terminal (blue)

**Show:** Bottom center panel.

**Say:**
> "At the bottom is **Output and Terminal** — logs, errors, and command-line tools."

**Do (click each tab slowly):**

1. Click **Problems** — "Problems shows errors and warnings from your code."
2. Click **Output** — "Output shows logs from builds and extensions."
3. Click **Terminal** (or `Ctrl + `` ` ``) — "Terminal runs commands — git, npm, Python, whatever you need."
4. If Terminal is open, type `echo hello` and Enter — "Commands run right inside Cursor."

**Say:**
> "When something breaks or you run a script, this is where you look."

---

### 1:50 – 2:30 | AI Assistant (purple)

**Show:** Right panel — Agent / Chat.

**Say:**
> "On the right is the **AI Assistant** — Cursor's chat and agent. This is what makes Cursor different from regular VS Code."

**Do:**

1. Point at the **prompt box** — "Type questions or tasks here."
2. Explain placeholders: "`@` references files; `/` runs skills and commands."
3. Point at **Agent** toggle — "Agent mode lets the AI edit files and run steps for you."
4. Point at **Auto** — "Auto picks the model."
5. Type a short, safe prompt and send, e.g.:
   > "What does this project folder structure do? Keep it to 3 bullets."

6. Wait for a short reply (or cut the recording if it's slow — see note below).

**Say (while or after it responds):**
> "The AI reads your project, suggests code, fixes bugs, and can make changes directly when Agent is on."

---

### 2:30 – 2:50 | How it fits together (optional live demo)

**Show:** Full window again.

**Say:**
> "Typical flow: pick a file in the Explorer, edit in the Editor, run or check results in the Terminal, and ask the AI when you're stuck."

**Do (quick sequence, ~15 sec):**

1. Click a file in Explorer.
2. Glance at Editor.
3. Glance at Terminal/Output.
4. Glance at AI panel.

---

### 2:50 – 3:00 | Outro

**Show:** Full Cursor window, or the annotated screenshot one last time.

**Say:**
> "That's Cursor — Explorer, Editor, Output, and AI Assistant. Thanks for watching."

**Do:** Stop recording.

---

## If the AI reply is slow

- Record the prompt and send; **stop recording** when you see the typing indicator.
- Or use a **pre-run chat** before recording and scroll to show an existing answer during this section.
- Or skip the live prompt and only point at the UI controls (still under 3 min).

---

## Keyboard shortcuts cheat sheet (on screen or end card)

| Shortcut | Action |
|---|---|
| `Ctrl + B` | Toggle sidebar / Explorer |
| `Ctrl + `` ` `` | Toggle terminal |
| `Ctrl + P` | Quick open file |
| `Ctrl + L` or `Ctrl + I` | Focus AI chat (Cursor default may vary) |
| `Ctrl + S` | Save file |

---

## After recording

1. Trim dead air at the start/end (first 2 sec, last 2 sec).
2. Optional: add the annotated PNG as a 3-second title card.
3. Share the Loom link or export MP4.

**Reference assets in this repo:**

- Full annotated view: `assets/cursor-anatomy-annotated.png`
- Section highlights: `assets/cursor-section-1-file-explorer.png` through `cursor-section-4-ai-assistant.png`
