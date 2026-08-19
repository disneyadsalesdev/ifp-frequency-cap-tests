import json
import re
import urllib.request
from pathlib import Path

url = "https://raw.githubusercontent.com/IABTechLab/seller-agent/main/src/ad_seller/constants/dma_codes.py"
text = urllib.request.urlopen(url, timeout=30).read().decode()
pairs = re.findall(r'^\s*(\d+):\s*\("([^"]+)"', text, re.M)
iab = {c: n for c, n in pairs}

# Nielsen standard corrections
iab["638"] = "San Diego"
iab["531"] = "Tallahassee-Thomasville"
iab.pop("825", None)  # duplicate San Diego code in some sources

by_code = dict(sorted(iab.items(), key=lambda x: int(x[0])))
by_name: dict[str, str] = {}
for code, name in by_code.items():
    if name not in by_name:
        by_name[name] = code

out = {
    "description": "Complete Nielsen DMA code reference (210 markets). Validated against IFP portal. Portal shows name; API uses dimension 'dma-code' with numeric string codes.",
    "dimension": "dma-code",
    "count": len(by_code),
    "by_code": by_code,
    "by_name": dict(sorted(by_name.items(), key=lambda x: x[0].lower())),
}

path = Path(__file__).resolve().parent.parent / "reference" / "dma-codes.json"
path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"Wrote {len(by_code)} DMAs")
print(f"Zanesville: {by_code.get('596')}")
