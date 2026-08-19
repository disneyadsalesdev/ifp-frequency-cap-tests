"""Validate SharePoint chatbot config files and print agent build checklist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "docs" / "sharepoint-chatbot"
CONFIG = ROOT / "config"


def main() -> int:
    required = [
        ROOT / "it-request-template.md",
        ROOT / "copilot-studio-setup-guide.md",
        ROOT / "teams-deployment-guide.md",
        ROOT / "team-quick-start.md",
        CONFIG / "agent-system-instructions.txt",
        CONFIG / "knowledge-sources.json",
        CONFIG / "sample-topics.json",
    ]
    missing = [p for p in required if not p.exists()]
    if missing:
        print("MISSING files:")
        for p in missing:
            print(f"  - {p}")
        return 1

    instructions = (CONFIG / "agent-system-instructions.txt").read_text(encoding="utf-8")
    ks = json.loads((CONFIG / "knowledge-sources.json").read_text(encoding="utf-8"))
    topics = json.loads((CONFIG / "sample-topics.json").read_text(encoding="utf-8"))

    print("SharePoint chatbot pack — validation OK\n")
    print(f"  Site URL: {ks.get('siteUrl')}")
    print(f"  Libraries: {len(ks.get('libraries', []))}")
    print(f"  System instructions: {len(instructions)} chars")
    print(f"  Test prompts: {len(topics.get('testPrompts', []))}")
    print("\nNext steps:")
    print("  1. Send it-request-template.md to IT")
    print("  2. Follow copilot-studio-setup-guide.md")
    print("  3. Follow teams-deployment-guide.md")
    print("  4. Share team-quick-start.md with your team")
    return 0


if __name__ == "__main__":
    sys.exit(main())
