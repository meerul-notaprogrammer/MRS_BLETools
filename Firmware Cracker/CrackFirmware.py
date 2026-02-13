"""
Firmware Cracker - Standalone Launcher
=======================================
Connects to sensor and extracts ALL firmware intelligence:
- Network endpoints (UDP/TCP, IPs, Ports)
- Device identity (IMEI, IMSI, ICCID)
- AT command capabilities
- Hidden configurations
"""

import subprocess
import sys
import os

# Auto-install required packages
def install_packages():
    required = ['bleak']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"[SETUP] Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])

install_packages()

import asyncio
from bleak import BleakScanner, BleakClient
from FirmwareIntelligence import FirmwareIntelligence, Colors


async def scan_for_sensors():
    """Scan for BLE devices"""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}SCANNING FOR SENSORS...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    devices = await BleakScanner.discover(timeout=5.0)
    
    if not devices:
        print(f"{Colors.RED}[ERROR] No devices found!{Colors.RESET}")
        return None
    
    print(f"{Colors.GREEN}Found {len(devices)} devices:{Colors.RESET}\n")
    
    for i, device in enumerate(devices, 1):
        name = device.name or "(Unknown)"
        print(f"  {i}. {name:<30} {device.address}")
    
    print(f"\n{Colors.YELLOW}Select device number: {Colors.RESET}", end="")
    try:
        choice = int(input().strip())
        if 1 <= choice <= len(devices):
            return devices[choice - 1]
    except:
        pass
    
    return None


async def main():
    """Main cracker function"""
    os.system('')  # Enable ANSI colors on Windows
    
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         FIRMWARE CRACKER v1.0                                 ║")
    print("║                    Extract ALL Sensor Intelligence                            ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Scan for devices
    device = await scan_for_sensors()
    
    if not device:
        print(f"{Colors.RED}[ERROR] No device selected{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}[SELECTED] {device.name} ({device.address}){Colors.RESET}")
    print(f"{Colors.YELLOW}[CONNECTING]...{Colors.RESET}")
    
    # Connect to device
    async with BleakClient(device.address, timeout=30.0) as client:
        print(f"{Colors.GREEN}[CONNECTED]{Colors.RESET}")
        
        # Discover services
        print(f"\n{Colors.CYAN}[DISCOVERING SERVICES]...{Colors.RESET}")
        
        write_char = None
        notify_char = None
        
        # Nordic UART Service UUIDs
        UART_RX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
        UART_TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
        
        for service in client.services:
            for char in service.characteristics:
                # Look for Nordic UART Service
                if char.uuid.lower() == UART_RX_UUID.lower():
                    write_char = char.uuid
                    print(f"{Colors.GREEN}[FOUND] Write characteristic: {char.uuid}{Colors.RESET}")
                
                if char.uuid.lower() == UART_TX_UUID.lower():
                    notify_char = char.uuid
                    print(f"{Colors.GREEN}[FOUND] Notify characteristic: {char.uuid}{Colors.RESET}")
                
                # Fallback: find any writable/notifiable characteristics
                if not write_char and ('write' in char.properties):
                    write_char = char.uuid
                
                if not notify_char and ('notify' in char.properties or 'indicate' in char.properties):
                    notify_char = char.uuid
        
        if not write_char or not notify_char:
            print(f"{Colors.RED}[ERROR] Could not find required characteristics{Colors.RESET}")
            return
        
        # Create intelligence scanner
        scanner = FirmwareIntelligence(client, write_char, notify_char)
        
        # Run full intelligence scan
        intelligence = await scanner.run_full_intelligence_scan()
        
        print(f"\n{Colors.GREEN}[COMPLETE] Firmware intelligence extraction complete!{Colors.RESET}")
        print(f"{Colors.DIM}Check the reports folder for detailed JSON output{Colors.RESET}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[EXIT] Scan interrupted{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {e}{Colors.RESET}")
