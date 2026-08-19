"""Parse Notion loadPageChunk and download all images."""

import json
import re
from pathlib import Path

import httpx

PAGE = "2ecb74f3-3238-8084-b424-f411bbbf719b"
OUT = Path(__file__).resolve().parent / "pptx_assets" / "notion_cursor_walkthrough"
HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


def block_value(block: dict) -> dict:
    val = block.get("value", {})
    if isinstance(val, dict) and "value" in val and isinstance(val["value"], dict):
        return val["value"]
    return val if isinstance(val, dict) else {}


def load_all_chunks() -> dict:
    cursor = {"stack": []}
    chunk_number = 0
    merged_blocks: dict = {}
    while True:
        resp = httpx.post(
            "https://99fold.notion.site/api/v3/loadPageChunk",
            json={
                "pageId": PAGE,
                "limit": 100,
                "cursor": cursor,
                "chunkNumber": chunk_number,
                "verticalColumns": False,
            },
            headers=HEADERS,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        blocks = data.get("recordMap", {}).get("block", {})
        merged_blocks.update(blocks)
        cursor = data.get("cursor", {})
        stack = cursor.get("stack") or []
        print(f"chunk {chunk_number}: blocks={len(blocks)}, stack depth={len(stack)}")
        if not stack:
            break
        chunk_number += 1
        if chunk_number > 20:
            break
    return merged_blocks


def text_from_props(props: dict, key: str = "title") -> str:
    parts = props.get(key) or []
    return "".join(p[0] for p in parts if p)


def extract_content(blocks: dict) -> list[dict]:
    items: list[dict] = []
    for bid, block in blocks.items():
        val = block_value(block)
        btype = val.get("type")
        props = val.get("properties") or {}
        if btype == "image":
            src = text_from_props(props, "source")
            caption = text_from_props(props, "caption")
            if src:
                items.append({"type": "image", "id": bid, "url": src, "caption": caption})
        elif btype in ("header", "sub_header", "sub_sub_header"):
            text = text_from_props(props, "title")
            if text:
                items.append({"type": btype, "id": bid, "text": text})
        elif btype in ("text", "bulleted_list", "numbered_list", "toggle"):
            text = text_from_props(props, "title")
            if text:
                items.append({"type": btype, "id": bid, "text": text})
    return items


def notion_image_url(src: str, block_id: str) -> str:
    if src.startswith("http"):
        return src
    from urllib.parse import quote

    return (
        f"https://99fold.notion.site/image/{quote(src, safe='')}"
        f"?table=block&id={block_id}&cache=v2"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    blocks = load_all_chunks()
    (OUT / "all_blocks.json").write_text(json.dumps(blocks, indent=2)[:500000], encoding="utf-8")
    content = extract_content(blocks)
    images = [c for c in content if c["type"] == "image"]
    print(f"content items: {len(content)}, images: {len(images)}")
    for img in images:
        print(f"  image: {img.get('caption') or img['url'][:60]}")

    saved = []
    with httpx.Client(timeout=120, headers=HEADERS, follow_redirects=True) as client:
        for i, img in enumerate(images, 1):
            url = notion_image_url(img["url"], img["id"])
            path = OUT / f"walkthrough_{i:02d}.png"
            try:
                r = client.get(url)
                r.raise_for_status()
                path.write_bytes(r.content)
                saved.append(path)
                print(f"saved {path.name} {len(r.content)} bytes")
            except Exception as exc:
                print(f"fail {url[:80]}: {exc}")

    manifest = {"images": images, "content": content, "saved": [str(p) for p in saved]}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"done: {len(saved)} images")


if __name__ == "__main__":
    main()
