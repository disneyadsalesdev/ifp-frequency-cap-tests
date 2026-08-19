# Training deck screenshots

**New hires:** read **[START-HERE.md](../START-HERE.md)** first.

Save PNGs here, then rebuild:

```powershell
cd C:\Users\syeda012\projects\ifp-frequency-cap-tests\docs
py build_deck.py
# or: py build_deck.py -o "$env:USERPROFILE\Downloads\Cursor_Training_Guide.pptx"
```

The deck slide **What to Screenshot — Instructions** is the master list. Filenames must match exactly.

---

## GeeksforGeeks infographics (bundled in deck)

These are copied into the deck automatically from `docs/images/`:

| File | Slide |
|------|--------|
| `gfg-what-is-cursor.png` | What Is Cursor AI? |
| `gfg-key-features.png` | Key Features of Cursor AI |
| `gfg-limitations-advantages.png` | Limitations vs Advantages |
| `gfg-real-life-applications.png` | Real-Life Applications |

Source article: [GeeksforGeeks — How to use Cursor AI](https://www.geeksforgeeks.org/blogs/how-to-use-cursor-ai-with-examples/)

---

## IFP practice lab (required for trainers)

Open **ifp-frequency-cap-tests**, run Steps 1–5 from slide **IFP Practice — Copy These Prompts**.

| Filename | Must show in the image |
|----------|-------------------------|
| `00-ifp-open-folder.png` | **File → Open Folder** dialog; **ifp-frequency-cap-tests** selected; **Open** visible |
| `00-ifp-ask-cap-json.png` | **Ask** mode; Step 1 prompt; answer about `cap-ratio-expectations.json` |
| `00-ifp-dma-lookup.png` | Step 2 prompt; reply with **Baton Rouge DMA number** (e.g. 716) |
| `00-ifp-at-mention.png` | `@` menu open; `reference/cap-ratio-expectations.json` or `dma-codes.json` in list |
| `00-ifp-agent-notes.png` | **Agent** mode; Step 4 prompt; **practice-notes.md** in sidebar |
| `00-ifp-diff-accept.png` | Diff on **practice-notes.md**; **Accept** and **Reject** visible |
| `00-ifp-forecast.png` | *(Optional Step 5, VPN)* forecast prompt + capacity / available / ratio |
| `02-agent-chat.png` | Chat open; **Agent** mode selected; no secrets |

---

## Team workflows (optional)

| Filename | Must show |
|----------|-----------|
| `04-daily-report-prompt.png` | `Run @dailypublisherscript.py` + success in chat |
| `06-outlook-draft.png` | Outlook draft after daily report |

(`05-forecast.png` is redundant if you captured `00-ifp-forecast.png`.)

---

## Tips

- Crop tight; one Cursor theme; redact internal URLs and numbers if required.
- ~1200–1400 px wide PNG; Win+Shift+S on Windows.
