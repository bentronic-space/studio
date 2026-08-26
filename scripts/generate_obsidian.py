from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
DEVICES = ROOT / "data" / "devices"
CONNECTIONS = ROOT / "data" / "connections"
OUTPUT = ROOT / "docs" / "Geräte"
INDEX = ROOT / "docs" / "Geräte.md"

OUTPUT.mkdir(parents=True, exist_ok=True)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# --------------------------------------------------
# Load devices
# --------------------------------------------------

devices = {}

for path in sorted(DEVICES.glob("*.yaml")):
    device = load_yaml(path)
    device_id = device.get("id")

    if device_id:
        devices[device_id] = device


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def device_name(device_id):
    return devices.get(device_id, {}).get("name", device_id)


def port_name(device_id, port_id):
    device = devices.get(device_id, {})

    for port in device.get("ports", []):
        if port.get("id") == port_id:
            return port.get("name", port_id)

    return port_id


def obsidian_link(device_id):
    name = device_name(device_id)
    return f"[[Geräte/{device_id}|{name}]]"


def format_list(values):
    if not values:
        return "Keine"

    return "\n".join(f"- {value}" for value in values)


# --------------------------------------------------
# Load connections
# --------------------------------------------------

connections = []

for path in sorted(CONNECTIONS.glob("*.yaml")):
    connection = load_yaml(path)

    if connection.get("status") == "active":
        connections.append(connection)


# --------------------------------------------------
# Generate device page
# --------------------------------------------------

def generate_device_page(device):
    device_id = device.get("id", "unknown")
    name = device.get("name", device_id)
    device_type = device.get("type", "unknown")
    status = device.get("status", "unknown")
    location = device.get("location", "unknown")

    capabilities = device.get("capabilities", {})
    technical = capabilities.get("technical", [])
    musical = capabilities.get("musical", [])

    ports = device.get("ports", [])

    incoming = []
    outgoing = []

    for connection in connections:
        source = connection.get("source", {})
        target = connection.get("target", {})

        if source.get("device") == device_id:
            outgoing.append(connection)

        if target.get("device") == device_id:
            incoming.append(connection)

    content = f"""# {name}

**ID:** `{device_id}`  
**Typ:** {device_type}  
**Status:** {status}  
**Ort:** {location}

## Technische Fähigkeiten

{format_list(technical)}

## Musikalische Fähigkeiten

{format_list(musical)}

## Anschlüsse

"""

    if ports:
        for port in ports:
            port_id = port.get("id", "unknown")
            display_name = port.get("name", port_id)
            port_type = port.get("type", "unknown")
            direction = port.get("direction", "unknown")

            content += (
                f"- **{display_name}** (`{port_id}`) – "
                f"{port_type}, {direction}\n"
            )
    else:
        content += "Keine Anschlüsse erfasst.\n"

    content += "\n## Verbindungen\n\n"

    content += "### Ausgänge\n\n"

    if outgoing:
        for connection in outgoing:
            source = connection.get("source", {})
            target = connection.get("target", {})
            signal = connection.get("signal", {})
            cable = connection.get("cable", {})

            target_device = target.get("device")
            target_port = target.get("port")

            line = (
                f"- **{port_name(source.get('device'), source.get('port'))}** → "
                f"{obsidian_link(target_device)} / "
                f"{port_name(target_device, target_port)} "
                f"— `{signal.get('transport', 'unknown')}`"
            )

            cable_id = cable.get("id")

            if cable_id:
                line += f" — Kabel `{cable_id}`"

            content += line + "\n"
    else:
        content += "Keine aktiven Ausgänge.\n"

    content += "\n### Eingänge\n\n"

    if incoming:
        for connection in incoming:
            source = connection.get("source", {})
            target = connection.get("target", {})
            signal = connection.get("signal", {})
            cable = connection.get("cable", {})

            line = (
                f"- {obsidian_link(source.get('device'))} / "
                f"{port_name(source.get('device'), source.get('port'))} → "
                f"**{port_name(target.get('device'), target.get('port'))}** "
                f"— `{signal.get('transport', 'unknown')}`"
            )

            cable_id = cable.get("id")

            if cable_id:
                line += f" — Kabel `{cable_id}`"

            content += line + "\n"
    else:
        content += "Keine aktiven Eingänge.\n"

    content += "\n## Notizen\n\n"

    notes = device.get("notes", [])

    if notes:
        content += format_list(notes) + "\n"
    else:
        content += "Keine Notizen.\n"

    return content


# --------------------------------------------------
# Generate device pages
# --------------------------------------------------

generated = 0

for device_id in sorted(devices):
    device = devices[device_id]

    output_file = OUTPUT / f"{device_id}.md"

    output_file.write_text(
        generate_device_page(device),
        encoding="utf-8"
    )

    generated += 1
    print(f"Generated: {output_file}")


# --------------------------------------------------
# Generate device index
# --------------------------------------------------

groups = {}

for device_id in sorted(devices):
    device = devices[device_id]

    device_type = device.get("type", "other")
    groups.setdefault(device_type, []).append(device_id)


content = """# Geräte

> Automatisch aus `data/devices/*.yaml` generiert.

"""

for device_type in sorted(groups):
    content += f"## {device_type.title()}\n\n"

    for device_id in groups[device_type]:
        content += f"- {obsidian_link(device_id)}\n"

    content += "\n"


INDEX.write_text(content, encoding="utf-8")

print(f"Generated: {INDEX}")
print()
print(f"Generated {generated} device pages.")
print(f"Loaded {len(connections)} active connections.")
