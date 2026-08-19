# Clone instructions — Mac & Windows

Share **these two clone URLs** with your team (replace placeholders after you push to your git host).

| Repo | Clone URL (fill in after push) |
|------|--------------------------------|
| IFP tests + docs | `https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-frequency-cap-tests.git` |
| MCP server | `https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-mcp-server.git` |

Same URLs work on **Windows and Mac**.

---

## Windows (PowerShell)

```powershell
mkdir C:\Users\YourName\projects -ErrorAction SilentlyContinue
cd C:\Users\YourName\projects

git clone https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-frequency-cap-tests.git
git clone https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-mcp-server.git

py -m pip install -r C:\Users\YourName\projects\ifp-mcp-server\requirements.txt
```

Create `C:\Users\YourName\.cursor\mcp.json` from `docs/templates/mcp.json` (replace `YourName`).

Cursor → **Open Folder** → `ifp-frequency-cap-tests` → Reload → MCP **green**.

---

## Mac (Terminal)

```bash
mkdir -p ~/projects
cd ~/projects

git clone https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-frequency-cap-tests.git
git clone https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-mcp-server.git

python3 -m pip install -r ~/projects/ifp-mcp-server/requirements.txt
```

Create `/Users/YourName/.cursor/mcp.json` from `docs/templates/mcp.mac.json` (replace `YourName`).

Cursor → **Open Folder** → `ifp-frequency-cap-tests` → Reload → MCP **green**.

---

## Trainer: push repos (one time)

Repos are initialized locally. After creating empty repos on your git server:

**Windows (PowerShell)** — from `docs/scripts/push-both-repos.ps1` or manually:

```powershell
# ifp-frequency-cap-tests
cd C:\Users\YourName\projects\rym-work\ifp-frequency-cap-tests
git remote add origin https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-frequency-cap-tests.git
git push -u origin main

# ifp-mcp-server
cd C:\Users\YourName\projects\rym-work\ifp-mcp-server
git remote add origin https://YOUR-GIT-SERVER/YOUR-TEAM/ifp-mcp-server.git
git push -u origin main
```

**Cursor-hosted repos (Mac or Linux only):** install [origin CLI](https://cursor.com/docs), run `origin auth login`, then `origin repo create ifp-frequency-cap-tests` and repeat for `ifp-mcp-server`.

---

## Update later

Inside each repo folder:

```bash
git pull
```

---

## No git access?

Send individual files (see NEW-USER-SIMPLE-GUIDE Part B) or ask IT for repo read access.
