# Logitech Z407 Control Tool (macOS)

A simple Python tool to control Logitech Z407 speakers from macOS, specifically designed to replace the functionality of a lost wireless dial.

## Features
- **Switch Inputs**: Toggle between Bluetooth, Aux (3.5mm), and USB.
- **Volume Control**: Adjust the internal speaker volume (independent of PC volume).
- **Pairing Mode**: Force the speakers into Bluetooth pairing mode.
- **Factory Reset**: Reset the speakers to resolve connection issues.

## Prerequisites
- macOS
- Python 3
- `bleak` library

## Installation
1.  Open Terminal.
2.  Install the required library:
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage
Run the script from your terminal:
```bash
python3 z407_control.py
```
Follow the on-screen prompts to select your desired action.

### Menu Options
1.  **Bluetooth Input**: Switch to Bluetooth source.
2.  **Aux (3.5mm)**: Switch to the 3.5mm cable input.
3.  **USB**: Switch to the Micro-USB input (**Recommended for PC**).
4.  **Force Pairing Mode**: Make the speakers discoverable (fast blue blink).
5.  **Volume Up**: Increase internal volume (prompts for number of steps).
6.  **Volume Down**: Decrease internal volume.
7.  **Factory Reset**: Reset speaker settings.
8.  **Play/Pause**: Toggle mute/unmute or play/pause (useful if audio is silent).

## Interpreting Output
- **c103**: Switched to USB.
- **c102**: Switched to Aux.
- **c101**: Switched to Bluetooth.
- **c200**: Enabled Pairing Mode.

## Troubleshooting
- **No Sound on USB**: ensure you are using a **Data** Micro-USB cable, not a "Charge Only" cable.
- **"Bluetooth turned off"**: Enable Bluetooth on your Mac.
- **Script finds nothing**: Unplug speakers from power for 10 seconds and retry.
