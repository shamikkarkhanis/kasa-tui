import asyncio
import sys
from typing import Dict, Optional, List, Any
from kasa import Discover

class KasaTUI:
    def __init__(self):
        self.devices: Dict[str, Any] = {}
        self.device_list: List[Any] = []
        self.running = True

    async def discover_devices(self):
        print("Scanning for devices... please wait.")
        try:
            found = await Discover.discover()
            self.devices = found
            self.device_list = list(found.values())
            if self.device_list:
                await asyncio.gather(*[d.update() for d in self.device_list])
            print(f"Discovery complete. Found {len(self.device_list)} devices.")
            self.list_devices()
        except Exception as e:
            print(f"Error during discovery: {e}")

    def list_devices(self):
        if not self.device_list:
            print("No devices found. Try /scan")
            return

        print("\n--- Device List ---")
        for idx, device in enumerate(self.device_list):
            try:
                state = "ON" if device.is_on else "OFF"
                info = f"[{idx + 1}] {device.alias:<20} ({device.host}) - {state}"
                
                # Try to get brightness from light module or fallback
                bri = None
                if device.modules and "light" in device.modules:
                    light = device.modules["light"]
                    if getattr(light, "is_dimmable", False):
                        bri = getattr(light, "brightness", None)
                elif getattr(device, "is_dimmable", False):
                     bri = getattr(device, "brightness", None)
                
                if bri is not None:
                    info += f" [Bright: {bri}%]"
                
                print(info)
            except Exception as e:
                print(f"[{idx + 1}] {device.host} - Error: {e}")

        print("-------------------")

    def get_device(self, identifier: str) -> Optional[Any]:
        if identifier.isdigit():
            idx = int(identifier) - 1
            if 0 <= idx < len(self.device_list):
                return self.device_list[idx]
        
        for device in self.device_list:
            if device.host == identifier:
                return device
        
        identifier_lower = identifier.lower()
        for device in self.device_list:
            if identifier_lower in device.alias.lower():
                return device
        
        return None

    async def handle_command(self, command_line: str):
        parts = command_line.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        # Remove optional leading slash if user still types it
        if cmd.startswith("/"):
            cmd = cmd[1:]
            
        args = parts[1:]

        if cmd in ["quit", "exit"]:
            self.running = False
            print("Goodbye!")
        
        elif cmd == "scan":
            await self.discover_devices()

        elif cmd == "list":
            self.list_devices()

        elif cmd == "debug":
             if not args:
                print("Usage: debug <id|name|ip>")
                return
             target = " ".join(args)
             device = self.get_device(target)
             if device:
                 print(f"Debug info for {device.alias}:")
                 print(f"  Type: {type(device)}")
                 print(f"  Modules: {device.modules.keys() if device.modules else 'None'}")
                 if device.modules:
                     for name, mod in device.modules.items():
                         print(f"    Module '{name}': {type(mod)}")
                         print(f"      dir: {dir(mod)}")
                 print(f"  Dir(device): {dir(device)}")
             else:
                 print("Device not found.")

        elif cmd == "on":
            if not args:
                print("Usage: on <id|name|ip>")
                return
            target = " ".join(args)
            device = self.get_device(target)
            if device:
                print(f"Turning on {device.alias}...")
                await device.turn_on()
                await device.update()
                print(f"{device.alias} is now ON.")
            else:
                print(f"Device '{target}' not found.")

        elif cmd == "off":
            if not args:
                print("Usage: off <id|name|ip>")
                return
            target = " ".join(args)
            device = self.get_device(target)
            if device:
                print(f"Turning off {device.alias}...")
                await device.turn_off()
                await device.update()
                print(f"{device.alias} is now OFF.")
            else:
                print(f"Device '{target}' not found.")

        elif cmd == "dim":
            if len(args) < 2:
                print("Usage: dim <id|name|ip> <level 0-100>")
                return
            
            try:
                level = int(args[-1])
                target = " ".join(args[:-1])
            except ValueError:
                print("Level must be a number.")
                return

            if not (0 <= level <= 100):
                print("Level must be between 0 and 100.")
                return

            device = self.get_device(target)
            if device:
                print(f"Setting {device.alias} brightness to {level}%...")
                
                # Attempt to set brightness via module or fallback
                try:
                    if device.modules and "light" in device.modules:
                        await device.modules["light"].set_brightness(level)
                    else:
                        # Fallback for older devices or if module structure differs
                        await device.set_brightness(level)
                    
                    await device.update()
                    print(f"{device.alias} brightness set.")
                except Exception as e:
                    print(f"Failed to set brightness: {e}")
                    print("This device might not support dimming or is incompatible with the current method.")

            else:
                print(f"Device '{target}' not found.")

        elif cmd == "help":
            print("\nAvailable commands:")
            print("  scan             - Discover devices")
            print("  list             - List cached devices")
            print("  on <target>      - Turn device ON")
            print("  off <target>     - Turn device OFF")
            print("  dim <target> <%> - Set brightness (e.g., dim 1 50)")
            print("  debug <target>   - Inspect device object")
            print("  exit             - Exit")
            print("  <target> can be the List ID, IP address, or Name.")
        
        else:
            print("Unknown command. Type help for options.")

    async def run(self):
        print("Welcome to Kasa TUI")
        await self.discover_devices()
        print("Type /help for commands.")

        while self.running:
            try:
                print("> ", end="", flush=True)
                cmd = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not cmd:
                    break
                await self.handle_command(cmd)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    tui = KasaTUI()
    try:
        asyncio.run(tui.run())
    except KeyboardInterrupt:
        pass
