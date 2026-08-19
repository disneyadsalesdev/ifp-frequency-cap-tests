"""Fetch images from a public Notion page for training deck import."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import httpx

NOTION_URL = (
    "https://99fold.notion.site/Understanding-Cursor-A-Graphical-Walkthrough-of-the-Cursor-IDE-"
    "2ecb74f332388084b424f411bbbf719b"
)
PAGE_ID = "2ecb74f3-3238-8084-b424-f411bbbf719b"
ASSETS_DIR = Path(__file__).resolve().parent / "pptx_assets" / "notion_cursor_walkthrough"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}


def extract_urls_from_html(html: str) -> list[str]:
    patterns = [
        r"https://prod-files-secure\.s3\.us-west-2\.amazonaws\.com/[^\"\\]+",
        r"https://[^\"\\]+\.amazonaws\.com/[^\"\\]+",
        r"https://www\.notion\.so/image/[^\"\\]+",
        r"https://[^\"\\]+\.(?:png|jpg|jpeg|webp)(?:\?[^\"\\]*)?",
    ]
    found: list[str] = []
    for pat in patterns:
        for match in re.findall(pat, html, flags=re.IGNORECASE):
            url = unquote(match.rstrip("\\"))
            if url not in found:
                found.append(url)
    return found


def fetch_via_notion_api() -> list[dict]:
    """Try Notion internal API for public pages."""
    api_url = "https://www.notion.so/api/v3/loadPageChunk"
    payload = {
        "pageId": PAGE_ID,
        "limit": 100,
        "cursor": {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False,
    }
    with httpx.Client(timeout=60.0, headers=HEADERS) as client:
        resp = client.post(api_url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    records = data.get("recordMap", {})
    blocks = records.get("block", {}).get("value", {})
    images: list[dict] = []
    for block_id, block in blocks.items():
        val = block.get("value", {})
        btype = val.get("type")
        if btype == "image":
            src = (val.get("properties") or {}).get("source", [[""]])[0][0]
            caption = (val.get("properties") or {}).get("caption", [[""]])[0][0]
            if src:
                images.append({"id": block_id, "url": src, "caption": caption, "type": btype})
        elif btype in ("header", "sub_header", "sub_sub_header", "text", "bulleted_list", "numbered_list"):
            text_parts = (val.get("properties") or {}).get("title", [])
            text = "".join(part[0] for part in text_parts if part)
            if text.strip():
                images.append({"id": block_id, "text": text.strip(), "type": btype})
    return images


def download_images(urls: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    with httpx.Client(timeout=120.0, headers=HEADERS, follow_redirects=True) as client:
        for i, url in enumerate(urls, start=1):
            ext = ".png"
            if ".jpg" in url.lower() or "jpeg" in url.lower():
                ext = ".jpg"
            elif ".webp" in url.lower():
                ext = ".webp"
            path = out_dir / f"notion_{i:02d}{ext}"
            try:
                r = client.get(url)
                r.raise_for_status()
                path.write_bytes(r.content)
                saved.append(path)
                print(f"  saved {path.name} ({len(r.content)} bytes)")
            except httpx.HTTPError as exc:
                print(f"  skip {url[:80]}... ({exc})")
    return saved


def main() -> int:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = ASSETS_DIR / "notion_content.json"

    content: list[dict] = []
    image_urls: list[str] = []

    print("Trying Notion API...")
    try:
        content = fetch_via_notion_api()
        meta_path.write_text(json.dumps(content, indent=2), encoding="utf-8")
        image_urls = [c["url"] for c in content if c.get("url")]
        print(f"  API blocks: {len(content)}, images: {len(image_urls)}")
    except Exception as exc:
        print(f"  API failed: {exc}")

    if not image_urls:
        print("Fetching HTML...")
        with httpx.Client(timeout=60.0, headers=HEADERS, follow_redirects=True) as client:
            html = client.get(NOTION_URL).text
        (ASSETS_DIR / "page.html").write_text(html, encoding="utf-8")
        image_urls = extract_urls_from_html(html)
        print(f"  HTML image URLs: {len(image_urls)}")

    if not image_urls:
        print("No images found.")
        return 1

    print("Downloading images...")
    saved = download_images(image_urls, ASSETS_DIR)
    print(f"Downloaded {len(saved)} images to {ASSETS_DIR}")
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
