import asyncio
import sys

try:
    from bleak import BleakScanner, BleakClient
except ImportError:
    print("Error: 'bleak' library not found.")
    print("Please install it using: pip install bleak")
    sys.exit(1)

# UUIDs from reverse engineering
SERVICE_UUID = "0000fdc2-0000-1000-8000-00805f9b34fb"
COMMAND_UUID = "c2e758b9-0e78-41e0-b0cb-98a593193fc5"
RESPONSE_UUID = "b84ac9c6-29c5-46d4-bba1-9d534784330f"

# Command constants
CMD_INPUT_BT = "8101"
CMD_INPUT_AUX = "8102"
CMD_INPUT_USB = "8103"
CMD_BT_PAIR = "8200"
CMD_VOL_UP = "8002"
CMD_VOL_DOWN = "8003"
CMD_BASS_UP = "8000"
CMD_BASS_DOWN = "8001"
CMD_FACTORY_RESET = "8300"
CMD_PLAY_PAUSE = "8004"

async def send_command(client, command_hex):
    """Sends a command to the Z407 speaker."""
    print(f"Sending command: {command_hex}...")
    await client.write_gatt_char(COMMAND_UUID, bytes.fromhex(command_hex), response=False)
    print("Command sent.")

async def notification_handler(sender, data):
    """Handles incoming notifications from the speaker."""
    print(f"Received response: {data.hex()}")

async def main():
    print("Scanning for Logitech Z407...")
    devices = await BleakScanner.discover(service_uuids=[SERVICE_UUID])
    
    # Filter for devices that look like the Z407 (by name or just because we filtered by service UUID)
    target_device = None
    for d in devices:
        # The service UUID filter usually is enough, but checking name helps confirm
        if d.name and "Z407" in d.name:
            target_device = d
            break
    
    if not target_device and devices:
        # If we didn't find one by name but found one by service UUID, use the first one
        target_device = devices[0]

    if not target_device:
        print("Error: Could not find Logitech Z407 speakers.")
        print("Ensure they are plugged in and within range.")
        return

    print(f"Found device: {target_device.name} ({target_device.address})")

    # Determine functionality based on arguments or prompt
    print("\nSelect Action:")
    print("1. Bluetooth Input")
    print("2. Aux (3.5mm Cable)")
    print("3. USB (Micro USB Cable)")
    print("4. Force Bluetooth Pairing Mode")
    print("5. Volume Up (+)")
    print("6. Volume Down (-)")
    print("7. Bass Up (+)")
    print("8. Bass Down (-)")
    print("9. Play/Pause (Toggle Mute)")
    print("0. Factory Reset")
    
    choice = input("Enter choice (0-9): ").strip()
    
    command = None
    loop_count = 1
    
    if choice == "1":
        command = CMD_INPUT_BT
        print("Switching to Bluetooth Input...")
    elif choice == "2":
        command = CMD_INPUT_AUX
        print("Switching to Aux...")
    elif choice == "3":
        command = CMD_INPUT_USB
        print("Switching to USB...")
    elif choice == "4":
        command = CMD_BT_PAIR
        print("Activating Bluetooth Pairing Mode...")
    elif choice == "5":
        command = CMD_VOL_UP
        # Volume steps are small, let's allow multiple increments
        try:
            loop_count = int(input("How many steps (default 5)? ") or "5")
        except:
            loop_count = 5
        print(f"Increasing volume by {loop_count} steps...")
    elif choice == "6":
        command = CMD_VOL_DOWN
        try:
            loop_count = int(input("How many steps (default 5)? ") or "5")
        except:
            loop_count = 5
        print(f"Decreasing volume by {loop_count} steps...")
    elif choice == "7":
        command = CMD_BASS_UP
        try:
            loop_count = int(input("How many steps (default 1)? ") or "1")
        except:
            loop_count = 1
        print(f"Increasing Bass by {loop_count} steps...")
    elif choice == "8":
        command = CMD_BASS_DOWN
        try:
            loop_count = int(input("How many steps (default 1)? ") or "1")
        except:
            loop_count = 1
        print(f"Decreasing Bass by {loop_count} steps...")
    elif choice == "9":
        command = CMD_PLAY_PAUSE
        print("Toggling Play/Pause/Mute...")
    elif choice == "0":
        command = CMD_FACTORY_RESET
        print("WARNING: Factory Resetting Speakers...")
    else:
        print("Invalid choice.")
        return

    print(f"Connecting to {target_device.name}...")
    async with BleakClient(target_device.address) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        
        print("Connected!")
        
        # Subscribe to notifications to see responses
        await client.start_notify(RESPONSE_UUID, notification_handler)
        
        # Handshake
        await send_command(client, "8405")
        await asyncio.sleep(1.0) 
        
        if command:
            for _ in range(loop_count):
                await send_command(client, command)
                await asyncio.sleep(0.2) # Short delay between volume steps
            
            # Wait a bit to receive any response/confirmation
            await asyncio.sleep(1.0)
            print("Command execution complete.")
            
        await client.stop_notify(RESPONSE_UUID)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
