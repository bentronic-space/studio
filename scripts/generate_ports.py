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
# Build port usage
# --------------------------------------------------

port_usage = {}

for connection in connections:
    source = connection["source"]
    target = connection["target"]

    source_key = (source["device"], source["port"])
    target_key = (target["device"], target["port"])

    port_usage[source_key] = {
        "connection": connection,
        "role": "source",
    }

    port_usage[target_key] = {
        "connection": connection,
        "role": "target",
    }


# --------------------------------------------------
# Generate Markdown table
# --------------------------------------------------

lines = []

lines.append("# Studio Port Status")
lines.append("")
lines.append(
    "| Gerät | Port | Richtung | Anschluss | Transport | Status | Gegenstelle | Kabel |"
)
lines.append(
    "|---|---|---|---|---|---|---|---|"
)


for device_id in sorted(devices):
    device = devices[device_id]
    device_name = device.get("name", device_id)

    for port in device.get("ports", []):
        port_id = port["id"]
        port_name = port.get("name", port_id)

        direction = port.get("direction", "")
        connector = port.get("connector", "")
        transport = port.get("transport", "")

        key = (device_id, port_id)

        if key in port_usage:
            usage = port_usage[key]
            connection = usage["connection"]

            source = connection["source"]
            target = connection["target"]

            if usage["role"] == "source":
                other_device = target["device"]
            else:
                other_device = source["device"]

            cable = connection.get("cable" or {})
            cable_id = cable.get("id", "–")

            status = "🟢 belegt"
        else:
            other_device = "–"
            cable_id = "–"
            status = "⚪ frei"

        lines.append(
            f"| {device_name} | {port_name} | "
            f"{direction} | {connector} | {transport} | "
            f"{status} | {other_device} | {cable_id} |"
        )


# --------------------------------------------------
# Write output
# --------------------------------------------------

output_file = OUTPUT / "port-status.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated: {output_file}")
