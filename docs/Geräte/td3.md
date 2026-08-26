# Behringer TD-3

**ID:** `td3`  
**Typ:** synthesizer  
**Status:** active  
**Ort:** studio

## Technische Fähigkeiten

- midi
- midi_din
- midi_usb
- midi_thru
- sequencer
- cv
- gate
- sync
- external_filter_input

## Musikalische Fähigkeiten

- bass
- acid
- monophonic
- analog_synthesis

## Anschlüsse

- **MIDI IN** (`midi_in`) – midi, input
- **MIDI OUT** (`midi_out`) – midi, output
- **USB MIDI** (`midi_usb`) – midi, bidirectional
- **Power** (`midi_power`) – power, input
- **Audio OUT** (`audio_out`) – audio, output
- **Headphones** (`headphones_out`) – audio, output
- **Filter IN** (`filter_in`) – audio, input
- **Sync IN** (`sync_in`) – sync, input
- **CV OUT** (`cv_out`) – cv, output
- **GATE OUT** (`gate_out`) – gate, output

## Verbindungen

### Ausgänge

- **MIDI OUT** → [[Geräte/mpc_one|Akai MPC One]] / MIDI IN — `midi_din` — Kabel `midi_din_003`
- **Audio OUT** → [[Geräte/um300|Behringer UM300]] / Audio IN — `audio_analog` — Kabel `audio_patch_001`

### Eingänge

- [[Geräte/erica_midi_thru|Erica Synths MIDI Thru Box]] / MIDI THRU 1 → **MIDI IN** — `midi_din` — Kabel `midi_din_002`

## Notizen

- Digital Twin initial entry
- Audio output uses TRS connector but is unbalanced.
