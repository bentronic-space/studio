from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

devices = {}
errors = []
cables = {}

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------
# Load devices
# --------------------------------------------------

for path in sorted((DATA / "devices").glob("*.yaml")):
    data = load_yaml(path)

    device_id = data.get("id")

    if not device_id:
        errors.append(f"{path}: missing device id")
        continue

    if device_id in devices:
        errors.append(f"{path}: duplicate device id '{device_id}'")
        continue

    devices[device_id] = data

# --------------------------------------------------
# Load cables
# --------------------------------------------------

for path in sorted((DATA / "cables").glob("*.yaml")):
    data = load_yaml(path)

    cable_id = data.get("id")

    if not cable_id:
        errors.append(f"{path}: missing cable id")
        continue

    if cable_id in cables:
        errors.append(f"{path}: duplicate cable id '{cable_id}'")
        continue

    cables[cable_id] = data

# --------------------------------------------------
# Validate connections
# --------------------------------------------------

connection_count = 0

for path in sorted((DATA / "connections").glob("*.yaml")):
    connection = load_yaml(path)
    connection_count += 1

    source = connection.get("source", {})
    target = connection.get("target", {})

    source_device_id = source.get("device")
    source_port_id = source.get("port")

    target_device_id = target.get("device")
    target_port_id = target.get("port")

    # Cable
    cable = connection.get("cable", {})
    cable_id = cable.get("id") if isinstance(cable, dict) else cable

    if cable_id and cable_id not in cables:
        errors.append(
            f"{path}: cable '{cable_id}' does not exist"
        )

    # Source device
    if source_device_id not in devices:
        errors.append(
            f"{path}: source device '{source_device_id}' does not exist"
        )
        continue

    # Target device
    if target_device_id not in devices:
        errors.append(
            f"{path}: target device '{target_device_id}' does not exist"
        )
        continue

    source_device = devices[source_device_id]
    target_device = devices[target_device_id]

    source_port = next(
        (p for p in source_device.get("ports", [])
         if p.get("id") == source_port_id),
        None
    )

    target_port = next(
        (p for p in target_device.get("ports", [])
         if p.get("id") == target_port_id),
        None
    )

    # Source port
    if source_port is None:
        errors.append(
            f"{path}: source port "
            f"'{source_device_id}:{source_port_id}' does not exist"
        )
        continue

    # Target port
    if target_port is None:
        errors.append(
            f"{path}: target port "
            f"'{target_device_id}:{target_port_id}' does not exist"
        )
        continue

    # Direction
    if source_port.get("direction") not in ("output", "bidirectional"):
        errors.append(
            f"{path}: source port "
            f"'{source_device_id}:{source_port_id}' "
            f"is not an output"
        )

    if target_port.get("direction") not in ("input", "bidirectional"):
        errors.append(
            f"{path}: target port "
            f"'{target_device_id}:{target_port_id}' "
            f"is not an input"
        )

    # Transport compatibility
    source_transport = source_port.get("transport")
    target_transport = target_port.get("transport")

    signal_transport = connection.get("signal", {}).get("transport")

    if signal_transport:
        if source_transport and source_transport != signal_transport:
            errors.append(
                f"{path}: source transport mismatch "
                f"({source_transport} != {signal_transport})"
            )

        if target_transport and target_transport != signal_transport:
            errors.append(
                f"{path}: target transport mismatch "
                f"({target_transport} != {signal_transport})"
            )


# --------------------------------------------------
# Result
# --------------------------------------------------

print(f"Devices: {len(devices)}")
print(f"Connections: {connection_count}")

if errors:
    print()
    print("VALIDATION FAILED")
    print()

    for error in errors:
        print(f"ERROR: {error}")

    raise SystemExit(1)

print()
print("VALIDATION OK")
