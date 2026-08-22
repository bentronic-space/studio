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

# Devices
for device_id, device in devices.items():
    name = device.get("name", device_id)
    lines.append(f'    {device_id}["{name}"]')

lines.append("")

# Connections
for connection in connections:
    source = connection["source"]
    target = connection["target"]

    source_device = source["device"]
    source_port = source["port"]

    target_device = target["device"]
    target_port = target["port"]

    signal = connection.get("signal", {})
    signal_type = signal.get("type", "")
    transport = signal.get("transport", "")

    label = f"{source_port} → {target_port}"

    if signal_type:
        label += f"<br>{signal_type}"

    if transport:
        label += f"<br>{transport}"

    lines.append(
        f'    {source_device} -->|"{label}"| {target_device}'
    )

lines.append("")
lines.append("```")


# --------------------------------------------------
# Write output
# --------------------------------------------------

output_file = OUTPUT / "midi-routing.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated: {output_file}")
