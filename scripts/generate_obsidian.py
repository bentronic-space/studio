from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent

DEVICES = ROOT / "data" / "devices"
CONNECTIONS = ROOT / "data" / "connections"
CABLES = ROOT / "data" / "cables"

DEVICE_OUTPUT = ROOT / "docs" / "Geräte"
CABLE_OUTPUT = ROOT / "docs" / "Kabel"

DEVICE_INDEX = ROOT / "docs" / "Geräte.md"
CABLE_INDEX = ROOT / "docs" / "Kabel.md"

DEVICE_OUTPUT.mkdir(parents=True, exist_ok=True)
CABLE_OUTPUT.mkdir(parents=True, exist_ok=True)


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
# Load cables
# --------------------------------------------------

cables = {}

for path in sorted(CABLES.glob("*.yaml")):
    cable = load_yaml(path)
    cable_id = cable.get("id")

    if cable_id:
        cables[cable_id] = cable


# --------------------------------------------------
# Load active connections
# --------------------------------------------------

connections = []

for path in sorted(CONNECTIONS.glob("*.yaml")):
    connection = load_yaml(path)

    if connection.get("status") == "active":
        connections.append(connection)


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


def device_link(device_id):
    name = device_name(device_id)
    return f"[[Geräte/{device_id}|{name}]]"


def cable_link(cable_id):
    cable = cables.get(cable_id, {})
    name = cable.get("name", cable_id)

    return f"[[Kabel/{cable_id}|{name}]]"


def format_list(values):
    if not values:
        return "Keine"

    return "\n".join(f"- {value}" for value in values)


# --------------------------------------------------
# Connections belonging to a device
# --------------------------------------------------

def device_connections(device_id):
    incoming = []
    outgoing = []

    for connection in connections:
        source = connection.get("source", {})
        target = connection.get("target", {})

        if source.get("device") == device_id:
            outgoing.append(connection)

        if target.get("device") == device_id:
            incoming.append(connection)

    return incoming, outgoing


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

    incoming, outgoing = device_connections(device_id)

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
            cable_id = cable.get("id")

            line = (
                f"- **{port_name(source.get('device'), source.get('port'))}** → "
                f"{device_link(target_device)} / "
                f"{port_name(target_device, target_port)} "
                f"— `{signal.get('transport', 'unknown')}`"
            )

            if cable_id:
                if cable_id in cables:
                    line += f" — {cable_link(cable_id)}"
                else:
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

            cable_id = cable.get("id")

            line = (
                f"- {device_link(source.get('device'))} / "
                f"{port_name(source.get('device'), source.get('port'))} → "
                f"**{port_name(target.get('device'), target.get('port'))}** "
                f"— `{signal.get('transport', 'unknown')}`"
            )

            if cable_id:
                if cable_id in cables:
                    line += f" — {cable_link(cable_id)}"
                else:
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
# Generate cable page
# --------------------------------------------------

def cable_connections(cable_id):
    result = []

    for connection in connections:
        cable = connection.get("cable", {})

        if cable.get("id") == cable_id:
            result.append(connection)

    return result


def generate_cable_page(cable):
    cable_id = cable.get("id", "unknown")
    name = cable.get("name", cable_id)
    cable_type = cable.get("type", "unknown")
    transport = cable.get("transport", "")
    status = cable.get("status", "unknown")
    length = cable.get("length_m")

    content = f"""# {name}

**ID:** `{cable_id}`
**Typ:** {cable_type}
**Status:** {status}
"""

    if length is not None:
        content += f"**Länge:** {length} m\n"

    if transport:
        content += f"**Transport:** `{transport}`\n"

    color = cable.get("color")

    if color:
        content += f"**Farbe:** {color}\n"

    content += "\n## Stecker\n\n"

    connectors = cable.get("connectors")

    if connectors:
        content += (
            f"- Quelle: `{connectors.get('source', 'unknown')}`\n"
            f"- Ziel: `{connectors.get('target', 'unknown')}`\n"
        )
    else:
        connector_a = cable.get("connector_a")
        connector_b = cable.get("connector_b")

        if connector_a or connector_b:
            content += f"- A: `{connector_a or 'unknown'}`\n"
            content += f"- B: `{connector_b or 'unknown'}`\n"

    content += "\n## Aktuelle Verwendung\n\n"

    used_in = cable_connections(cable_id)

    if used_in:
        for connection in used_in:
            source = connection.get("source", {})
            target = connection.get("target", {})
            signal = connection.get("signal", {})

            source_device = source.get("device")
            target_device = target.get("device")

            content += (
                f"- {device_link(source_device)} / "
                f"{port_name(source_device, source.get('port'))}"
                f" → "
                f"{device_link(target_device)} / "
                f"{port_name(target_device, target.get('port'))}"
                f" — `{signal.get('transport', 'unknown')}`\n"
            )
    else:
        content += "Aktuell keiner aktiven Connection zugeordnet.\n"

    content += "\n## Notizen\n\n"

    notes = cable.get("notes", [])

    if notes:
        content += format_list(notes) + "\n"
    else:
        content += "Keine Notizen.\n"

    return content


# --------------------------------------------------
# Generate device pages
# --------------------------------------------------

generated_devices = 0

for device_id in sorted(devices):
    device = devices[device_id]

    output_file = DEVICE_OUTPUT / f"{device_id}.md"

    output_file.write_text(
        generate_device_page(device),
        encoding="utf-8"
    )

    generated_devices += 1


# --------------------------------------------------
# Generate device index
# --------------------------------------------------

groups = {}

for device_id in sorted(devices):
    device_type = devices[device_id].get("type", "other")
    groups.setdefault(device_type, []).append(device_id)


device_index_content = """# Geräte

> Automatisch aus `data/devices/*.yaml` generiert.

"""

for device_type in sorted(groups):
    device_index_content += f"## {device_type.title()}\n\n"

    for device_id in groups[device_type]:
        device_index_content += f"- {device_link(device_id)}\n"

    device_index_content += "\n"


DEVICE_INDEX.write_text(
    device_index_content,
    encoding="utf-8"
)


# --------------------------------------------------
# Generate cable pages
# --------------------------------------------------

generated_cables = 0

for cable_id in sorted(cables):
    cable = cables[cable_id]

    output_file = CABLE_OUTPUT / f"{cable_id}.md"

    output_file.write_text(
        generate_cable_page(cable),
        encoding="utf-8"
    )

    generated_cables += 1


# --------------------------------------------------
# Generate cable index
# --------------------------------------------------

cable_groups = {}

for cable_id in sorted(cables):
    cable_type = cables[cable_id].get("type", "other")
    cable_groups.setdefault(cable_type, []).append(cable_id)


cable_index_content = """# Kabel

> Automatisch aus `data/cables/*.yaml` generiert.

"""

for cable_type in sorted(cable_groups):
    cable_index_content += f"## {cable_type.title()}\n\n"

    for cable_id in cable_groups[cable_type]:
        cable_index_content += f"- {cable_link(cable_id)}\n"

    cable_index_content += "\n"


CABLE_INDEX.write_text(
    cable_index_content,
    encoding="utf-8"
)

# --------------------------------------------------
# Generate DMX overview
# --------------------------------------------------

DMX_INDEX = ROOT / "docs" / "DMX.md"


def generate_dmx_overview():
    dmx_devices = []

    for device_id, device in devices.items():
        current_dmx = device.get("current_dmx")

        if current_dmx:
            dmx_devices.append(
                (
                    current_dmx.get("start_address", 999),
                    device_id,
                    device,
                    current_dmx,
                )
            )

    dmx_devices.sort(key=lambda item: item[0])

    content = """# DMX

> Automatisch aus `data/devices/*.yaml`, `data/connections/*.yaml` und `data/cables/*.yaml` generiert.

## DMX-Kette

"""

    # Find the DMX chain starting at the USB-DMX interface
    dmx_connections = [
        connection
        for connection in connections
        if connection.get("signal", {}).get("type") == "dmx"
    ]

    current_device = "rixutech-usb-dmx-001"
    visited = set()

    content += f"{device_link(current_device)}\n\n"

    while current_device and current_device not in visited:
        visited.add(current_device)

        outgoing = [
            connection
            for connection in dmx_connections
            if connection.get("source", {}).get("device") == current_device
        ]

        if not outgoing:
            break

        connection = outgoing[0]

        target = connection.get("target", {})
        target_device = target.get("device")
        cable_id = connection.get("cable", {}).get("id")

        if cable_id and cable_id in cables:
            content += f"↓  {cable_link(cable_id)}\n\n"
        else:
            content += "↓  direkt verbunden\n\n"

        content += f"{device_link(target_device)}\n\n"

        current_device = target_device

    content += "## Aktuelle DMX-Konfiguration\n\n"

    if dmx_devices:
        content += "| Gerät | Modus | Startadresse | Adressbereich |\n"
        content += "|---|---:|---:|---:|\n"

        for _, device_id, device, current_dmx in dmx_devices:
            name = device.get("name", device_id)
            mode = current_dmx.get("mode", "unknown")
            start = current_dmx.get("start_address", "unknown")
            address_range = current_dmx.get("address_range", "unknown")

            content += (
                f"| {device_link(device_id)} | "
                f"{mode} | "
                f"{start} | "
                f"{address_range} |\n"
            )
    else:
        content += "Keine aktuellen DMX-Konfigurationen dokumentiert.\n"

    content += "\n## DMX-Geräte\n\n"

    for _, device_id, device, current_dmx in dmx_devices:
        content += f"### {device.get('name', device_id)}\n\n"

        content += (
            f"- Modus: `{current_dmx.get('mode', 'unknown')}`\n"
            f"- Startadresse: `{current_dmx.get('start_address', 'unknown')}`\n"
            f"- Adressbereich: `{current_dmx.get('address_range', 'unknown')}`\n"
        )

        content += "\n"

    content += "## Hinweise\n\n"
    content += (
        "- Die aktuelle Konfiguration wird über `current_dmx` "
        "in den Geräte-YAMLs dokumentiert.\n"
    )
    content += (
        "- Die technischen bzw. dokumentierten DMX-Modi bleiben "
        "im jeweiligen `dmx`-Abschnitt der Geräte-YAMLs erhalten.\n"
    )

    DMX_INDEX.write_text(content, encoding="utf-8")

    print(f"Generated: {DMX_INDEX}")


generate_dmx_overview()


# --------------------------------------------------
# Result
# --------------------------------------------------

print(f"Generated {generated_devices} device pages.")
print(f"Generated {generated_cables} cable pages.")
print(f"Loaded {len(connections)} active connections.")
print(f"Generated: {DEVICE_INDEX}")
print(f"Generated: {CABLE_INDEX}")
