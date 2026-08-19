"""Annotate a Cursor IDE screenshot with labeled section outline boxes."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

INPUT = Path(
    r"C:\Users\syeda012\.cursor\projects\c-Users-syeda012-projects-rym-work-ifp-frequency-cap-tests\assets\c__Users_syeda012_AppData_Roaming_Cursor_User_workspaceStorage_d7982efdbaf5229bbe2543ad2c759976_images_image-2b04b977-c9b2-4a76-b6cf-ec8ba129e3cd.png"
)
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "cursor-anatomy-annotated.png"

# Measured from screenshot pixels (1024x597)
Y_TOP = 35
Y_STATUS = 576
X_SIDEBAR = 182
X_AI = 624
Y_PANEL = 343

SECTIONS = [
    {
        "label": "FILE EXPLORER",
        "box": (0, Y_TOP, X_SIDEBAR, Y_STATUS),
        "color": (255, 80, 80),
    },
    {
        "label": "CODE EDITOR",
        "box": (X_SIDEBAR, Y_TOP, X_AI, Y_PANEL),
        "color": (80, 200, 180),
    },
    {
        "label": "OUTPUT / TERMINAL",
        "box": (X_SIDEBAR, Y_PANEL, X_AI, Y_STATUS),
        "color": (100, 180, 255),
    },
    {
        "label": "AI ASSISTANT",
        "box": (X_AI, Y_TOP, 1024, Y_STATUS),
        "color": (180, 120, 255),
    },
]


def is_red_pixel(px: np.ndarray) -> bool:
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    return r > 70 and g < 55 and b < 55


def remove_red_outline(arr: np.ndarray) -> np.ndarray:
    """Replace user-drawn red outline pixels with nearby background color."""
    cleaned = arr.copy()
    h, w = cleaned.shape[:2]
    red_mask = np.array([[is_red_pixel(cleaned[y, x]) for x in range(w)] for y in range(h)])

    for _ in range(4):
        for y in range(h):
            for x in range(w):
                if not red_mask[y, x]:
                    continue
                neighbors = []
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and not red_mask[ny, nx]:
                            neighbors.append(cleaned[ny, nx])
                if neighbors:
                    cleaned[y, x] = np.mean(neighbors, axis=0).astype(np.uint8)
                    red_mask[y, x] = False
    return cleaned


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_section(
    base: Image.Image,
    label: str,
    box: tuple[int, int, int, int],
    color: tuple[int, int, int],
    label_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    x1, y1, x2, y2 = box

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=(*color, 40))
    base.paste(Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB"))

    draw = ImageDraw.Draw(base)
    draw.rectangle((x1, y1, x2 - 1, y2 - 1), outline=color, width=3)

    text_bbox = draw.textbbox((0, 0), label, font=label_font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    pad_x, pad_y = 14, 8
    label_w = text_w + pad_x * 2
    label_h = text_h + pad_y * 2
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    lx1 = cx - label_w // 2
    ly1 = cy - label_h // 2

    draw.rectangle(
        (lx1, ly1, lx1 + label_w, ly1 + label_h),
        fill=(255, 255, 255),
        outline=(0, 0, 0),
        width=3,
    )
    draw.text((lx1 + pad_x, ly1 + pad_y - 2), label, fill=(0, 0, 0), font=label_font)


def main() -> None:
    source = np.array(Image.open(INPUT).convert("RGB"))
    cleaned = remove_red_outline(source)
    img = Image.fromarray(cleaned)
    label_font = load_font(18)

    for section in SECTIONS:
        draw_section(
            img,
            section["label"],
            section["box"],
            section["color"],
            label_font,
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, quality=95)
    print(f"Saved annotated image to: {OUTPUT}")


if __name__ == "__main__":
    main()
