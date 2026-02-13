import subprocess
import sys
import os

# Auto-install required packages
def install_packages():
    required = ['bleak', 'requests']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"[SETUP] Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
            print(f"[SETUP] {package} installed!")

install_packages()

import asyncio
import re
import requests
from bleak import BleakClient, BleakScanner
from datetime import datetime
import logging
import msvcrt  # Windows keyboard input

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Nordic UART Service UUIDs (preferred for commands)
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# NHR API Headers (from documentation)
NHR_HEADERS = {
    "Content-Type": "application/json",
    "Nietzsche-API-KEY": "NHR-IOT-SENSOR",
    "User-Agent": "NHR-Sensor-Bridge/1.0"
}

# ANSI Colors for professional output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("  ███╗   ███╗██████╗ ███████╗    ██████╗ ██╗     ███████╗  ████████╗ ██████╗  ██████╗ ██╗     ███████╗")
    print("  ████╗ ████║██╔══██╗██╔════╝    ██╔══██╗██║     ██╔════╝  ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝")
    print("  ██╔████╔██║██████╔╝███████╗    ██████╔╝██║     █████╗       ██║   ██║   ██║██║   ██║██║     ███████╗")
    print("  ██║╚██╔╝██║██╔══██╗╚════██║    ██╔══██╗██║     ██╔══╝       ██║   ██║   ██║██║   ██║██║     ╚════██║")
    print("  ██║ ╚═╝ ██║██║  ██║███████║    ██████╔╝███████╗███████╗     ██║   ╚██████╔╝╚██████╔╝███████╗███████║")
    print("  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚══════╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝")
    print(f"{Colors.RESET}")
    print(f"{Colors.GREEN}  >>>  {Colors.YELLOW}Scan{Colors.RESET} | {Colors.YELLOW}Read{Colors.RESET} | {Colors.YELLOW}Command{Colors.RESET} | {Colors.YELLOW}Post{Colors.GREEN}  <<<{Colors.RESET}")
    print(f"{Colors.DIM}  Version 0.1.2 - Professional BLE + HTTP Scanner{Colors.RESET}")
    print()
    print(f"{Colors.CYAN}{'=' * 100}{Colors.RESET}")
    print()


class WastebinDataParser:
    """Parse wastebin sensor data and convert to NHR API format"""
    
    @staticmethod
    def parse_sensor_string(raw_str, device_imei="000000000000000"):
        """
        Parse sensor data string and return JSON payload for HTTP POST
        Expected format: temp:24.25 ,fill:76 ,batt:3.2
        Or fallback: temp:24.25 ,x:0.29 ,y:-88.43 ,z:-0.01
        """
        payload = {
            "cmd": "RP",
            "device": device_imei,
            "battery": "0",
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "dIndex": "0410",
            "data": "0"
        }
        
        try:
            # Try to parse fill level
            fill_match = re.search(r'fill[:\s]*(\d+)', raw_str, re.IGNORECASE)
            if fill_match:
                payload["data"] = fill_match.group(1)
            
            # Try to parse temperature
            temp_match = re.search(r'temp[:\s]*([\d.]+)', raw_str, re.IGNORECASE)
            if temp_match:
                payload["temperature"] = temp_match.group(1)
            
            # Try to parse battery
            batt_match = re.search(r'batt[:\s]*([\d.]+)', raw_str, re.IGNORECASE)
            if batt_match:
                payload["battery"] = batt_match.group(1)
            
            # For tilt sensors (x, y, z) - calculate fill level from tilt
            x_match = re.search(r'x[:\s]*([-\d.]+)', raw_str, re.IGNORECASE)
            y_match = re.search(r'y[:\s]*([-\d.]+)', raw_str, re.IGNORECASE)
            z_match = re.search(r'z[:\s]*([-\d.]+)', raw_str, re.IGNORECASE)
            
            if y_match and not fill_match:
                # Y-axis close to -90 means upright/empty, close to 0 means tilted/full
                y_val = abs(float(y_match.group(1)))
                # Convert tilt to fill percentage (rough estimate)
                if y_val > 80:
                    fill_pct = min(100, int((90 - y_val) * 10))
                else:
                    fill_pct = min(100, int(100 - y_val))
                payload["data"] = str(max(0, fill_pct))
                payload["tilt_y"] = y_match.group(1)
            
            if x_match:
                payload["tilt_x"] = x_match.group(1)
            if z_match:
                payload["tilt_z"] = z_match.group(1)
                
        except Exception as e:
            logger.warning(f"Parse error: {e}")
        
        return payload


class HTTPForwarder:
    """Handle HTTP POST to server"""
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.success_count = 0
        self.error_count = 0
        self.last_status = None
        self.enabled = True
        
    def send(self, payload):
        """Send data to server and return result"""
        if not self.enabled:
            return None
            
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=NHR_HEADERS,
                timeout=10
            )
            
            self.last_status = response.status_code
            
            if response.status_code in [200, 201]:
                self.success_count += 1
                return {
                    "success": True,
                    "status": response.status_code,
                    "response": response.text[:100]
                }
            else:
                self.error_count += 1
                return {
                    "success": False,
                    "status": response.status_code,
                    "error": response.text[:200]
                }
                
        except requests.exceptions.Timeout:
            self.error_count += 1
            return {"success": False, "status": 0, "error": "Connection timeout"}
        except requests.exceptions.ConnectionError as e:
            self.error_count += 1
            return {"success": False, "status": 0, "error": f"Connection failed: {str(e)[:50]}"}
        except Exception as e:
            self.error_count += 1
            return {"success": False, "status": 0, "error": str(e)[:100]}


class BLEScanner:
    """Main BLE Scanner Tool"""
    
    def __init__(self):
        self.client = None
        self.device = None
        self.message_count = 0
        self.command_mode = False
        self.running = True
        self.write_chars = []
        self.notify_chars = []
        self.primary_write_char = None
        self.add_crlf = True
        
        # HTTP forwarding
        self.http_forwarder = None
        self.device_imei = "000000000000000"
        self.parser = WastebinDataParser()
        
    def notification_handler(self, sender, data):
        """Handle incoming BLE data"""
        if not data:
            return
        
        self.message_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        raw_str = data.decode('utf-8', errors='ignore').strip()
        
        if not self.command_mode:
            print(f"\n{Colors.CYAN}{'=' * 72}{Colors.RESET}")
            print(f"{Colors.GREEN}[RX #{self.message_count:04d}]{Colors.RESET} | {Colors.DIM}{timestamp}{Colors.RESET}")
            print(f"{Colors.CYAN}{'-' * 72}{Colors.RESET}")
            
            if raw_str:
                print(f"  {Colors.YELLOW}DATA:{Colors.RESET} {raw_str[:60]}")
            print(f"  {Colors.YELLOW}HEX: {Colors.RESET} {data.hex()[:50]}")
            
            # HTTP POST if enabled
            if self.http_forwarder and self.http_forwarder.enabled:
                payload = self.parser.parse_sensor_string(raw_str, self.device_imei)
                result = self.http_forwarder.send(payload)
                
                if result:
                    if result["success"]:
                        print(f"\n  {Colors.GREEN}[HTTP 200]{Colors.RESET} Sent to server")
                        print(f"  {Colors.DIM}Payload: {payload}{Colors.RESET}")
                    else:
                        print(f"\n  {Colors.RED}[HTTP {result['status']}]{Colors.RESET} {result['error']}")
                        
        else:
            # Compact mode
            print(f"{Colors.DIM}[{timestamp}] {raw_str[:50]}{Colors.RESET}")
            
    async def send_command(self, command, char_uuid=None):
        """Send command to BLE device"""
        if not self.client or not self.client.is_connected:
            print(f"{Colors.RED}[ERROR] Not connected{Colors.RESET}")
            return False
        
        target_char = char_uuid or self.primary_write_char
        
        if not target_char:
            print(f"{Colors.RED}[ERROR] No write characteristic available{Colors.RESET}")
            return False
        
        try:
            if self.add_crlf:
                cmd_bytes = (command + '\r\n').encode('utf-8')
            else:
                cmd_bytes = command.encode('utf-8')
            
            try:
                await self.client.write_gatt_char(target_char, cmd_bytes, response=False)
            except:
                await self.client.write_gatt_char(target_char, cmd_bytes, response=True)
            
            print(f"{Colors.GREEN}[TX] {command}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Send failed: {e}{Colors.RESET}")
            return False
    
    async def connect(self, device_info):
        """Connect to selected BLE device"""
        address = device_info.address
        name = device_info.name or "Unknown"
        
        print(f"\n{Colors.YELLOW}[CONNECTING] {name} ({address})...{Colors.RESET}")
        
        self.client = BleakClient(address, timeout=30.0)
        await self.client.connect()
        
        print(f"{Colors.GREEN}[CONNECTED] Successfully connected{Colors.RESET}")
        
        # Try to extract IMEI from device name (format: N_XXXX_XXXXX_XXXXXX)
        if name:
            imei_match = re.search(r'_(\d{6})$', name)
            if imei_match:
                self.device_imei = "351469520" + imei_match.group(1)
                print(f"{Colors.DIM}  Extracted IMEI: {self.device_imei}{Colors.RESET}")
        
        # Discover services
        print(f"\n{Colors.CYAN}[SERVICES] Discovering...{Colors.RESET}")
        print(f"{'-' * 72}")
        
        for service in self.client.services:
            print(f"\n  {Colors.BOLD}Service: {service.uuid}{Colors.RESET}")
            if service.description:
                print(f"  {Colors.DIM}{service.description}{Colors.RESET}")
            
            for char in service.characteristics:
                props = ', '.join(char.properties)
                print(f"    {Colors.DIM}|-- {char.uuid} ({props}){Colors.RESET}")
                
                if 'notify' in char.properties or 'indicate' in char.properties:
                    self.notify_chars.append(char.uuid)
                
                if 'write' in char.properties or 'write-without-response' in char.properties:
                    self.write_chars.append(char.uuid)
                    if char.uuid.lower() == UART_RX_CHAR_UUID.lower():
                        self.primary_write_char = char.uuid
        
        if not self.primary_write_char and self.write_chars:
            protected = ['00002a00', '00002a01', '00002a04', '00002aa6']
            for char in self.write_chars:
                if not any(p in char.lower() for p in protected):
                    self.primary_write_char = char
                    break
        
        print(f"{'-' * 72}")
        
        # Enable notifications
        print(f"\n{Colors.YELLOW}[NOTIFICATIONS] Enabling...{Colors.RESET}")
        enabled_count = 0
        
        for char_uuid in self.notify_chars:
            try:
                await self.client.start_notify(char_uuid, self.notification_handler)
                print(f"  {Colors.GREEN}[OK]{Colors.RESET} {char_uuid}")
                enabled_count += 1
            except Exception as e:
                print(f"  {Colors.RED}[FAIL]{Colors.RESET} {char_uuid}")
        
        print(f"\n{Colors.GREEN}[READY] {enabled_count} notification(s) active{Colors.RESET}")
        
        self.device = device_info
    
    async def disconnect(self):
        """Disconnect from device"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print(f"\n{Colors.YELLOW}[DISCONNECTED]{Colors.RESET}")
    
    async def setup_http_mode(self):
        """Setup HTTP forwarding mode"""
        print(f"\n{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        print(f"{Colors.BOLD}HTTP FORWARDING MODE{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        
        if self.http_forwarder and self.http_forwarder.enabled:
            print(f"\n{Colors.YELLOW}HTTP forwarding is currently ENABLED{Colors.RESET}")
            print(f"  URL: {self.http_forwarder.api_url}")
            print(f"  Success: {self.http_forwarder.success_count}")
            print(f"  Errors: {self.http_forwarder.error_count}")
            print(f"\n  1. Disable HTTP forwarding")
            print(f"  2. Change URL")
            print(f"  3. Back to receive mode")
            
            choice = input(f"\n{Colors.YELLOW}Choice [1-3]: {Colors.RESET}").strip()
            
            if choice == "1":
                self.http_forwarder.enabled = False
                print(f"{Colors.GREEN}[DISABLED] HTTP forwarding disabled{Colors.RESET}")
            elif choice == "2":
                url = input(f"{Colors.YELLOW}Enter new API URL: {Colors.RESET}").strip()
                if url:
                    self.http_forwarder.api_url = url
                    print(f"{Colors.GREEN}[UPDATED] URL changed to: {url}{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}Enable HTTP forwarding?{Colors.RESET}")
            print(f"{Colors.DIM}Data will be POSTed to your server in NHR API format{Colors.RESET}")
            print(f"\nExample URL: http://192.168.1.111:5000/api/sensor")
            
            url = input(f"\n{Colors.YELLOW}Enter API URL (or blank to cancel): {Colors.RESET}").strip()
            
            if url:
                # Test connection first
                print(f"\n{Colors.YELLOW}[TESTING] Connecting to {url}...{Colors.RESET}")
                
                test_payload = {
                    "cmd": "TEST",
                    "device": self.device_imei,
                    "battery": "4.2",
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "dIndex": "0410",
                    "data": "0"
                }
                
                try:
                    response = requests.post(url, json=test_payload, headers=NHR_HEADERS, timeout=5)
                    
                    if response.status_code in [200, 201]:
                        print(f"{Colors.GREEN}[SUCCESS] Server responded: {response.status_code}{Colors.RESET}")
                        self.http_forwarder = HTTPForwarder(url)
                        print(f"{Colors.GREEN}[ENABLED] HTTP forwarding is now active{Colors.RESET}")
                    else:
                        print(f"{Colors.YELLOW}[WARNING] Server returned: {response.status_code}{Colors.RESET}")
                        print(f"  Response: {response.text[:100]}")
                        enable = input(f"\n{Colors.YELLOW}Enable anyway? [y/N]: {Colors.RESET}").strip().lower()
                        if enable == 'y':
                            self.http_forwarder = HTTPForwarder(url)
                            print(f"{Colors.GREEN}[ENABLED] HTTP forwarding is now active{Colors.RESET}")
                            
                except requests.exceptions.ConnectionError:
                    print(f"{Colors.RED}[ERROR] Cannot connect to {url}{Colors.RESET}")
                    print(f"{Colors.DIM}Make sure the server is running and accessible{Colors.RESET}")
                    enable = input(f"\n{Colors.YELLOW}Enable anyway? [y/N]: {Colors.RESET}").strip().lower()
                    if enable == 'y':
                        self.http_forwarder = HTTPForwarder(url)
                        print(f"{Colors.GREEN}[ENABLED] HTTP forwarding enabled (will retry on data){Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}[MODE] Returning to receive mode...{Colors.RESET}")
    
    async def command_mode_handler(self):
        """Handle command mode input"""
        print(f"\n{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        print(f"{Colors.BOLD}MENU{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        print(f"\n  1. Send command to sensor")
        print(f"  2. HTTP forwarding mode {'[ACTIVE]' if self.http_forwarder and self.http_forwarder.enabled else '[OFF]'}")
        print(f"  3. Toggle CR+LF (currently: {'ON' if self.add_crlf else 'OFF'})")
        print(f"  4. Back to receive mode")
        print(f"  5. Quit")
        
        choice = input(f"\n{Colors.YELLOW}Choice [1-5]: {Colors.RESET}").strip()
        
        if choice == "1":
            # Command mode
            print(f"\n{Colors.DIM}Type command to send (blank to cancel):{Colors.RESET}")
            cmd = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
            if cmd:
                await self.send_command(cmd)
                await asyncio.sleep(0.5)
                
        elif choice == "2":
            await self.setup_http_mode()
            
        elif choice == "3":
            self.add_crlf = not self.add_crlf
            print(f"{Colors.GREEN}[CONFIG] CR+LF {'enabled' if self.add_crlf else 'disabled'}{Colors.RESET}")
            
        elif choice == "5":
            self.running = False
            return
        
        self.command_mode = False
    
    async def run(self):
        """Main run loop"""
        print(f"\n{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        print(f"{Colors.BOLD}RECEIVE MODE{Colors.RESET} - Listening for sensor data 24/7")
        print(f"{Colors.DIM}   Press Ctrl+P for menu, Ctrl+C to exit{Colors.RESET}")
        if self.http_forwarder and self.http_forwarder.enabled:
            print(f"{Colors.GREEN}   HTTP POST: {self.http_forwarder.api_url}{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 72}{Colors.RESET}")
        
        try:
            while self.running:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\x10':  # Ctrl+P
                        self.command_mode = True
                        await self.command_mode_handler()
                        # Reprint header after menu
                        print(f"\n{Colors.CYAN}{'=' * 72}{Colors.RESET}")
                        print(f"{Colors.BOLD}RECEIVE MODE{Colors.RESET}")
                        if self.http_forwarder and self.http_forwarder.enabled:
                            print(f"{Colors.GREEN}   HTTP POST: {self.http_forwarder.api_url}{Colors.RESET}")
                        print(f"{Colors.CYAN}{'=' * 72}{Colors.RESET}")
                
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[STOPPING]...{Colors.RESET}")


async def scan_devices():
    """Live scan for BLE devices - shows devices as they appear"""
    print(f"\n{Colors.YELLOW}[SCANNING] Live scan - devices appear as discovered{Colors.RESET}")
    print(f"{Colors.DIM}   Press ENTER to stop scanning early...{Colors.RESET}\n")
    print(f"{'-' * 72}")
    print(f"  {'#':>3}  {'':2} {'Name':<25} {'Address':<20} {'Signal'}")
    print(f"{'-' * 72}")
    
    discovered_list = []  # Keep order of discovery
    discovered_addresses = set()  # For deduplication
    nhr_count = 0
    
    def detection_callback(device, advertisement_data):
        nonlocal nhr_count
        
        # Skip if already seen
        if device.address in discovered_addresses:
            return
        
        discovered_addresses.add(device.address)
        rssi = advertisement_data.rssi if advertisement_data else -100
        discovered_list.append((device, rssi))
        device_count = len(discovered_list)
        
        name = device.name if device.name else "(Unknown)"
        signal_bars = max(1, (rssi + 100) // 10)
        signal = '#' * signal_bars + '-' * (10 - signal_bars)
        
        is_nhr = device.name and "NHR" in device.name.upper()
        if is_nhr:
            nhr_count += 1
            
        marker = f"{Colors.GREEN}*{Colors.RESET}" if is_nhr else " "
        name_color = Colors.GREEN if is_nhr else Colors.RESET
        
        # Print device immediately with its index
        print(f"  {device_count:3d}. {marker} {name_color}{name:<25}{Colors.RESET} {device.address:<20} [{signal}] {rssi}dBm")
    
    # Start scanner with callback
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    
    # Scan for up to 5 seconds, but allow early stop
    try:
        for i in range(50):  # 5 seconds (50 x 0.1s)
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\r':  # Enter key
                    print(f"\n{Colors.YELLOW}[STOPPED] Scan stopped by user{Colors.RESET}")
                    break
            await asyncio.sleep(0.1)
    except:
        pass
    
    await scanner.stop()
    
    print(f"{'-' * 72}")
    
    if len(discovered_list) == 0:
        print(f"{Colors.RED}[ERROR] No devices found!{Colors.RESET}")
        return []
    
    print(f"\n{Colors.GREEN}[FOUND] {len(discovered_list)} devices{Colors.RESET}")
    if nhr_count > 0:
        print(f"{Colors.GREEN}[INFO] {nhr_count} NHR device(s) found (marked with *){Colors.RESET}")
    
    # Return in discovery order (same as displayed)
    return discovered_list


def show_agreement():
    """Show user agreement on first run"""
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}  USER AGREEMENT{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print()
    print(f"  {Colors.YELLOW}MRS BLE Tools V0.1.2{Colors.RESET}")
    print()
    print("  This tool is provided for development and testing purposes.")
    print("  By using this software, you agree to:")
    print()
    print("  1. Use this tool responsibly and legally")
    print("  2. Only connect to devices you own or have permission to access")
    print("  3. Not use for unauthorized data collection")
    print("  4. Accept that this software is provided AS-IS")
    print()
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    
    try:
        agree = input(f"\n{Colors.YELLOW}Do you agree? [Y/n]: {Colors.RESET}").strip().lower()
        if agree == 'n':
            print(f"\n{Colors.RED}[EXIT] Agreement declined{Colors.RESET}")
            return False
        return True
    except (EOFError, KeyboardInterrupt):
        return False


async def main():
    """Main function"""
    print_header()
    
    # Show agreement
    if not show_agreement():
        return
    
    print()
    
    # Ask about HTTP mode at startup
    print(f"{Colors.YELLOW}Do you want to enable HTTP forwarding at startup?{Colors.RESET}")
    print(f"{Colors.DIM}(You can also enable this later with Ctrl+P){Colors.RESET}")
    
    try:
        enable_http = input(f"\n{Colors.YELLOW}Enter API URL (or press ENTER to skip): {Colors.RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        enable_http = ""
    
    http_forwarder = None
    if enable_http:
        http_forwarder = HTTPForwarder(enable_http)
        print(f"{Colors.GREEN}[ENABLED] HTTP forwarding to: {enable_http}{Colors.RESET}")
    
    # Scan
    devices = await scan_devices()
    
    if not devices:
        return
    
    print(f"\n{Colors.YELLOW}Select device number (or ENTER for 1): {Colors.RESET}", end="", flush=True)
    try:
        device_input = input().strip()
        device_num = int(device_input) if device_input else 1
    except (ValueError, EOFError, KeyboardInterrupt):
        device_num = 1
        print(f"{Colors.DIM}(using device 1){Colors.RESET}")
    
    if device_num < 1 or device_num > len(devices):
        print(f"{Colors.RED}[ERROR] Invalid selection! Using device 1{Colors.RESET}")
        device_num = 1
    
    selected_device, selected_rssi = devices[device_num - 1]
    print(f"\n{Colors.GREEN}[SELECTED] {selected_device.name} ({selected_device.address}){Colors.RESET}")
    
    scanner = BLEScanner()
    if http_forwarder:
        scanner.http_forwarder = http_forwarder
    
    try:
        await scanner.connect(selected_device)
        await asyncio.sleep(1)
        await scanner.run()
        
    except KeyboardInterrupt:
        pass  # Silent exit
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {e}{Colors.RESET}")
    finally:
        await scanner.disconnect()
    
    # Print stats
    print(f"\n{Colors.CYAN}[STATS]{Colors.RESET}")
    print(f"  Messages received: {scanner.message_count}")
    if scanner.http_forwarder:
        print(f"  HTTP Success: {scanner.http_forwarder.success_count}")
        print(f"  HTTP Errors: {scanner.http_forwarder.error_count}")
    print(f"\n{Colors.GREEN}[EXIT] Goodbye{Colors.RESET}")


if __name__ == "__main__":
    os.system('')  # Enable ANSI colors on Windows
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[EXIT] Goodbye{Colors.RESET}")
    except EOFError:
        print(f"\n{Colors.YELLOW}[EXIT] Goodbye{Colors.RESET}")
    except Exception:
        print(f"\n{Colors.YELLOW}[EXIT] Goodbye{Colors.RESET}")

