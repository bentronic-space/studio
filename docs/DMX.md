# DMX

> Automatisch aus `data/devices/*.yaml`, `data/connections/*.yaml` und `data/cables/*.yaml` generiert.

## DMX-Kette

[[Geräte/rixutech-usb-dmx-001|RIXUTECH USB-DMX Interface]]

↓  [[Kabel/dmx-usb-interface-5m-001|Integrated DMX Cable 5m]]

[[Geräte/uking-zq01069-002|U'King ZQ01069 PAR 2]]

↓  [[Kabel/dmx-xlr-3m-001|DMX XLR Cable 3m]]

[[Geräte/uking-zq01069-001|U'King ZQ01069 PAR 1]]

↓  [[Kabel/dmx-xlr-2m-001|DMX XLR Cable 2m]]

[[Geräte/spinspot-001|Spinspot]]

↓  direkt verbunden

[[Geräte/dmx-terminator-120ohm-001|DMX 120 Ohm Terminator]]

## Aktuelle DMX-Konfiguration

| Gerät | Modus | Startadresse | Adressbereich |
|---|---:|---:|---:|
| [[Geräte/uking-zq01069-001|U'King ZQ01069 PAR 1]] | 4ch | 1 | 1-4 |
| [[Geräte/uking-zq01069-002|U'King ZQ01069 PAR 2]] | 4ch | 9 | 9-12 |
| [[Geräte/spinspot-001|Spinspot]] | 4ch | 13 | 13-16 |

## DMX-Geräte

### U'King ZQ01069 PAR 1

- Modus: `4ch`
- Startadresse: `1`
- Adressbereich: `1-4`

### U'King ZQ01069 PAR 2

- Modus: `4ch`
- Startadresse: `9`
- Adressbereich: `9-12`

### Spinspot

- Modus: `4ch`
- Startadresse: `13`
- Adressbereich: `13-16`

## Hinweise

- Die aktuelle Konfiguration wird über `current_dmx` in den Geräte-YAMLs dokumentiert.
- Die technischen bzw. dokumentierten DMX-Modi bleiben im jeweiligen `dmx`-Abschnitt der Geräte-YAMLs erhalten.
