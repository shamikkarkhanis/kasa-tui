import asyncio
from kasa import Discover

async def main():
    print("Discovering Kasa devices...")
    # Discover devices on the network
    found_devices = await Discover.discover()
    
    if not found_devices:
        print("No devices found.")
        return

    print(f"Found {len(found_devices)} devices:")
    for ip, device in found_devices.items():
        # Ensure we have the latest device information
        await device.update()
        print(f"  - {device.alias} ({ip}) - Model: {device.model}")

if __name__ == "__main__":
    asyncio.run(main())
