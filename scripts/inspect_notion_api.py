"""Inspect Notion API response for walkthrough page."""

import json
import re
from pathlib import Path

import httpx

PAGE = "2ecb74f3-3238-8084-b424-f411bbbf719b"
OUT = Path(__file__).resolve().parent / "pptx_assets" / "notion_cursor_walkthrough"

r = httpx.post(
    "https://99fold.notion.site/api/v3/loadPageChunk",
    json={
        "pageId": PAGE,
        "limit": 100,
        "cursor": {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False,
    },
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    timeout=60,
)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "loadPageChunk.json").write_text(r.text, encoding="utf-8")
data = r.json()
print("top keys:", list(data.keys()))
rm = data.get("recordMap") or {}
print("recordMap keys:", list(rm.keys()))
for k, v in rm.items():
    if isinstance(v, dict) and isinstance(v.get("value"), dict):
        print(f"  {k}: {len(v['value'])} entries")

text = r.text
print("type=image occurrences:", text.count('"type":"image"'))
urls = re.findall(r"https://[^\"\\]+prod-files-secure[^\"\\]+", text)
print("prod-files urls:", len(urls))
for u in urls[:10]:
    print(" ", u[:120])

# Parse blocks for images
blocks = rm.get("block", {}).get("value", {})
images = []
for bid, block in blocks.items():
    val = block.get("value", {})
    if val.get("type") == "image":
        src = (val.get("properties") or {}).get("source", [[""]])[0][0]
        images.append({"id": bid, "url": src})
print("parsed images:", len(images))
