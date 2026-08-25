from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = ROOT / "diagrams"

OUTPUT.mkdir(exist_ok=True)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------
# Load devices
# --------------------------------------------------

devices = {}

for path in sorted((DATA / "devices").glob("*.yaml")):
    data = load_yaml(path)
    devices[data["id"]] = data


# --------------------------------------------------
# Load connections
# --------------------------------------------------

connections = []

for path in sorted((DATA / "connections").glob("*.yaml")):
    connections.append(load_yaml(path))


# --------------------------------------------------
# Generate Mermaid
# --------------------------------------------------

lines = []

lines.append("```mermaid")
lines.append("flowchart LR")
lines.append("")

# Device nodes
for device_id, device in devices.items():
    name = device.get("name", device_id)
    lines.append(f'    {device_id}["{name}"]')

lines.append("")

# Connections
for index, connection in enumerate(connections):
    source = connection["source"]
    target = connection["target"]

    source_device = source["device"]
    target_device = target["device"]

    signal = connection.get("signal") or {}
    signal_type = signal.get("type", "")
    transport = signal.get("transport", "")

    if signal_type == "midi":
        label = "MIDI"
        class_name = "midi"
    elif signal_type == "audio":
        label = "AUDIO"
        class_name = "audio"
    else:
        label = signal_type.upper() if signal_type else "SIGNAL"
        class_name = "other"

    if transport:
        label += f"<br>{transport}"

    edge_id = f"edge{index}"

    lines.append(
        f'    {source_device} -->|"{label}"| {target_device}'
    )

lines.append("")

# Styling
lines.append("    linkStyle default stroke-width:2px;")

lines.append("```")


# --------------------------------------------------
# Write output
# --------------------------------------------------

output_file = OUTPUT / "midi-routing.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated: {output_file}")
