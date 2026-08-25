from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = ROOT / "diagrams"

OUTPUT.mkdir(exist_ok=True)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


cables = []

for path in sorted((DATA / "cables").glob("*.yaml")):
    cables.append(load_yaml(path))


lines = []

lines.append("# Cable Inventory")
lines.append("")
lines.append("| ID | Name | Typ | Transport | Farbe | Status |")
lines.append("|---|---|---|---|---|---|")

for cable in cables:
    cable_id = cable.get("id", "")
    name = cable.get("name", "")
    cable_type = cable.get("type", "")
    transport = cable.get("transport", "")
    color = cable.get("color", "")
    status = cable.get("status", "")

    lines.append(
        f"| {cable_id} | {name} | {cable_type} | "
        f"{transport} | {color} | {status} |"
    )


output_file = OUTPUT / "cable-inventory.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated: {output_file}")
