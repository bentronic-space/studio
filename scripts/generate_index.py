from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS = ROOT / "diagrams"
OUTPUT = ROOT / "studio.md"


def read(path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


routing = read(DIAGRAMS / "midi-routing.md")
ports = read(DIAGRAMS / "port-status.md")
cables = read(DIAGRAMS / "cable-inventory.md")


content = f"""# Studio

> Digital Twin – automatically generated overview

## Current Signal Routing

{routing}

## Port Status

{ports}

## Cable Inventory

{cables}

"""

OUTPUT.write_text(content, encoding="utf-8")

print(f"Generated: {OUTPUT}")
