"""
DEEP FIRMWARE CRACKER
=====================
Maximum depth extraction - get EVERYTHING:
- Kernel & bootloader info
- Complete AT command set (100+ commands)
- Memory & file system access
- Hardware capabilities
- Complete network configuration
- Protocol analysis
"""

import subprocess
import sys

# Auto-install
def install_packages():
    required = ['bleak']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])

install_packages()

import asyncio
import os
from bleak import BleakScanner, BleakClient
from DeepFirmwareExtractor import DeepFirmwareExtractor, Colors


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
    """Main deep extraction function"""
    os.system('')  # Enable ANSI colors
    
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    DEEP FIRMWARE CRACKER v2.0                                 ║")
    print("║                    MAXIMUM DEPTH EXTRACTION                                   ║")
    print("║                                                                               ║")
    print("║  Extracts:                                                                    ║")
    print("║  • Kernel & Bootloader Information                                           ║")
    print("║  • Complete AT Command Set (100+ commands)                                   ║")
    print("║  • Memory & File System Access                                               ║")
    print("║  • Hardware Capabilities                                                     ║")
    print("║  • Complete Network Configuration                                            ║")
    print("║  • Protocol & Timing Analysis                                                ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}⚠️  WARNING: This will probe 100+ AT commands{Colors.RESET}")
    print(f"{Colors.YELLOW}   Extraction time: ~5-10 minutes{Colors.RESET}")
    print(f"{Colors.YELLOW}   Keep device within BLE range{Colors.RESET}\n")
    
    proceed = input(f"{Colors.YELLOW}Continue? [Y/n]: {Colors.RESET}").strip().lower()
    if proceed == 'n':
        print(f"{Colors.RED}[CANCELLED]{Colors.RESET}")
        return
    
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
                if char.uuid.lower() == UART_RX_UUID.lower():
                    write_char = char.uuid
                    print(f"{Colors.GREEN}[FOUND] Write characteristic{Colors.RESET}")
                
                if char.uuid.lower() == UART_TX_UUID.lower():
                    notify_char = char.uuid
                    print(f"{Colors.GREEN}[FOUND] Notify characteristic{Colors.RESET}")
                
                # Fallback
                if not write_char and ('write' in char.properties):
                    write_char = char.uuid
                
                if not notify_char and ('notify' in char.properties or 'indicate' in char.properties):
                    notify_char = char.uuid
        
        if not write_char or not notify_char:
            print(f"{Colors.RED}[ERROR] Could not find required characteristics{Colors.RESET}")
            return
        
        # Create deep extractor
        extractor = DeepFirmwareExtractor(client, write_char, notify_char)
        
        # Run deep extraction
        print(f"\n{Colors.GREEN}[STARTING] Deep firmware extraction...{Colors.RESET}")
        print(f"{Colors.DIM}This will take several minutes. Please wait...{Colors.RESET}\n")
        
        extraction_data, report_file = await extractor.run_deep_extraction()
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.GREEN}[COMPLETE] Deep extraction finished!{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        if report_file:
            print(f"{Colors.CYAN}Report saved to:{Colors.RESET} {report_file}")
            print(f"\n{Colors.YELLOW}Next steps:{Colors.RESET}")
            print(f"  1. Review the JSON report for complete data")
            print(f"  2. Check FIRMWARE_DEVELOPMENT_GUIDE.md")
            print(f"  3. Use extracted info to build custom firmware")
        
        print(f"\n{Colors.DIM}Press Enter to exit...{Colors.RESET}")
        input()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[EXIT] Extraction interrupted{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {e}{Colors.RESET}")
