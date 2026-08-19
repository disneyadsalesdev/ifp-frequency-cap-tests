"""Generate docs/images/00-mcp-json.png — editor-style reference for training deck."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "images" / "00-mcp-json.png"

JSON_LINES = [
    "{",
    '  "mcpServers": {',
    '    "ifp-forecast": {',
    '      "type": "stdio",',
    '      "command": "py",',
    '      "args": ["C:/Users/YourName/projects/ifp-mcp-server/server.py"],',
    '      "env": {',
    '        "IFP_API_URL": "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast",',
    '        "IFP_SOURCE_HEADER": "RYM Frequency Cap Test",',
    '        "IFP_TESTS_ROOT": "C:/Users/YourName/projects/ifp-frequency-cap-tests"',
    "      }",
    "    }",
    "  }",
    "}",
]

# Simple syntax colors (Cursor-like dark theme)
COLORS = {
    "bg": (30, 30, 30),
    "tab_bar": (37, 37, 38),
    "tab_active": (30, 30, 30),
    "tab_inactive": (45, 45, 45),
    "text": (212, 212, 212),
    "key": (156, 220, 254),
    "string": (206, 145, 120),
    "brace": (212, 212, 212),
    "path_bar": (51, 51, 51),
    "path_text": (180, 180, 180),
    "highlight": (255, 200, 0),
}


def _font(size: int, mono: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/lucon.ttf",
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _colorize_line(line: str) -> list[tuple[str, tuple[int, int, int]]]:
    """Return (text, color) segments for one JSON line."""
    if not line.strip():
        return [(line, COLORS["text"])]
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]
    parts: list[tuple[str, tuple[int, int, int]]] = [(indent, COLORS["text"])]

    if stripped in ("{", "}", "},", "  },", "    },", "      }"):
        parts.append((stripped, COLORS["brace"]))
        return parts

    if ":" in stripped:
        key, _, rest = stripped.partition(":")
        parts.append((key, COLORS["key"]))
        parts.append((":", COLORS["text"]))
        rest = rest.rstrip()
        if "YourName" in rest:
            before, _, after = rest.partition("YourName")
            parts.append((before, COLORS["string"]))
            parts.append(("YourName", COLORS["highlight"]))
            parts.append((after, COLORS["string"]))
        else:
            parts.append((rest, COLORS["string"]))
        return parts

    parts.append((stripped, COLORS["text"]))
    return parts


def main() -> Path:
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    font = _font(18)
    font_sm = _font(14)
    font_tab = _font(13)

    # Tab bar
    draw.rectangle([0, 0, width, 36], fill=COLORS["tab_bar"])
    draw.rectangle([12, 6, 130, 34], fill=COLORS["tab_active"])
    draw.text((22, 10), "mcp.json", fill=COLORS["text"], font=font_tab)

    # Path breadcrumb
    draw.rectangle([0, 36, width, 68], fill=COLORS["path_bar"])
    path = r"C:\Users\YourName\.cursor\mcp.json  ← replace YourName with your Windows username"
    draw.text((16, 44), path, fill=COLORS["path_text"], font=font_sm)

    # Line numbers + code
    y = 88
    line_h = 26
    for i, line in enumerate(JSON_LINES, start=1):
        num = f"{i:2}"
        draw.text((16, y), num, fill=(100, 100, 100), font=font)
        x = 52
        for segment, color in _colorize_line(line):
            draw.text((x, y), segment, fill=color, font=font)
            try:
                x += draw.textlength(segment, font=font)
            except AttributeError:
                x += len(segment) * 10
        y += line_h

    # Footer note
    note = "Save this file → Ctrl+Shift+P → Reload Window in Cursor"
    draw.text((16, height - 36), note, fill=COLORS["highlight"], font=font_sm)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Created: {OUT} ({OUT.stat().st_size // 1024} KB)")
    return OUT


if __name__ == "__main__":
    main()
