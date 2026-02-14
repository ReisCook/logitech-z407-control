# Logitech Z407 Control

Python script to control Logitech Z407 speakers via Bluetooth LE. Replaces a lost wireless dial.
Works on macOS, Windows, Linux. Requires Bluetooth capability.

## Run
```bash
pip install bleak
python z407_control.py
```

## Menu
### Inputs
*   **1** Bluetooth
*   **2** Aux (3.5mm)
*   **3** USB (Micro-USB)

### Audio
*   **5** Volume Up
*   **6** Volume Down
*   **8** Play/Pause (Toggle Mute)

### System
*   **4** Force Pairing Mode
*   **7** Factory Reset

## Response Codes
*   `c101` Bluetooth Input
*   `c102` Aux Input
*   `c103` USB Input
*   `c200` Pairing Mode
