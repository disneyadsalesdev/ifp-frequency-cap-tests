"""Generate isolated Cursor section highlight images."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from annotate_cursor_screenshot import (
    INPUT,
    SECTIONS,
    draw_section,
    load_font,
    remove_red_outline,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def dim_outside_section(base: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """Darken everything outside the target section."""
    x1, y1, x2, y2 = box
    arr = np.array(base.convert("RGB"), dtype=np.float32)
    h, w = arr.shape[:2]

    mask = np.zeros((h, w), dtype=bool)
    mask[y1:y2, x1:x2] = True

    dimmed = arr.copy()
    dimmed[~mask] *= 0.35
    return Image.fromarray(dimmed.astype(np.uint8))


def render_section(section: dict) -> Image.Image:
    source = np.array(Image.open(INPUT).convert("RGB"))
    cleaned = remove_red_outline(source)
    img = dim_outside_section(Image.fromarray(cleaned), section["box"])
    draw_section(img, section["label"], section["box"], section["color"], load_font(18))
    return img


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    filenames = {
        "FILE EXPLORER": "cursor-section-1-file-explorer.png",
        "CODE EDITOR": "cursor-section-2-code-editor.png",
        "OUTPUT / TERMINAL": "cursor-section-3-output-terminal.png",
        "AI ASSISTANT": "cursor-section-4-ai-assistant.png",
    }

    for section in SECTIONS:
        output = ASSETS / filenames[section["label"]]
        render_section(section).save(output, quality=95)
        print(f"Saved {output}")


if __name__ == "__main__":
    main()
