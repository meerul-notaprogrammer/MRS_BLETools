"""
Firmware Intelligence Tool
==========================
Extracts all possible information from the sensor firmware via BLE
- Network configuration (UDP/TCP/IP/Ports)
- Device identity (IMEI, IMSI, firmware version)
- AT command capabilities
- Hidden configurations
"""

import asyncio
import re
from datetime import datetime
from bleak import BleakClient
import json


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


class FirmwareIntelligence:
    """Extract all possible information from sensor firmware"""
    
    # Comprehensive AT command probe list
    AT_COMMANDS = {
        # Device Identity
        'identity': [
            'AT+CGMI',      # Manufacturer
            'AT+CGMM',      # Model
            'AT+CGMR',      # Firmware version
            'AT+CGSN',      # IMEI
            'AT+CIMI',      # IMSI
            'AT+CCID',      # ICCID (SIM card ID)
            'AT+ICCID',     # Alternative ICCID
            'ATI',          # Device info
        ],
        
        # Network Status
        'network': [
            'AT+COPS?',     # Operator selection
            'AT+CREG?',     # Network registration (GSM)
            'AT+CGREG?',    # Network registration (GPRS)
            'AT+CEREG?',    # Network registration (EPS/LTE)
            'AT+CSQ',       # Signal quality
            'AT+QCSQ',      # Extended signal quality
            'AT+QNWINFO',   # Network info
            'AT+QENG="servingcell"',  # Serving cell info
        ],
        
        # PDP/Network Configuration
        'pdp_config': [
            'AT+CGDCONT?',  # PDP context definition
            'AT+CGACT?',    # PDP context activation state
            'AT+CGPADDR',   # Show PDP addresses
            'AT+NETOPEN?',  # Network open status
            'AT+IPADDR',    # Get local IP address
        ],
        
        # Socket/Connection Info (CRITICAL!)
        'socket_config': [
            'AT+CIPOPEN?',  # Current socket connections
            'AT+CIPSTATUS', # Connection status
            'AT+CIPSHOW?',  # Show remote IP and port
            'AT+NETSTAT',   # Network statistics
            'AT+QISTATE',   # Query socket service status
            'AT+QIACT?',    # Query PDP context status
        ],
        
        # Signal and Cell Info
        'signal': [
            'AT+QCBCINFOSC',  # Cell info (RSRP, SNR, etc)
            'AT+QCSTATUS?',   # Query status
            'AT+QNBIOTEVENT?', # NB-IoT event
        ],
        
        # Power and Sleep
        'power': [
            'AT+QCSLEEP?',  # Sleep mode status
            'AT+CPSMS?',    # Power saving mode
            'AT+CEDRXS?',   # eDRX settings
        ],
        
        # Configuration and Settings
        'config': [
            'AT&V',         # Display current configuration
            'AT+CMEE?',     # Error reporting mode
            'AT+QCFG="band"',      # Band configuration
            'AT+QCFG="nwscanmode"', # Network scan mode
            'AT+QCFG="iotopmode"',  # IoT operation mode
        ],
        
        # Custom/Vendor Specific
        'vendor': [
            'AT+QVERSION',  # Firmware version (Quectel)
            'AT+QHWVER',    # Hardware version
            'AT+QSCLK?',    # Sleep mode
        ],
    }
    
    def __init__(self, client: BleakClient, write_char_uuid: str, notify_char_uuid: str):
        self.client = client
        self.write_char = write_char_uuid
        self.notify_char = notify_char_uuid
        self.response_buffer = []
        self.waiting_for_response = False
        self.response_timeout = 3.0
        self.intelligence_data = {}
        
    def notification_handler(self, sender, data):
        """Capture all responses"""
        if data:
            try:
                text = data.decode('utf-8', errors='ignore').strip()
                if text:
                    self.response_buffer.append(text)
            except:
                pass
    
    async def send_at_command(self, command: str, timeout: float = 3.0) -> list:
        """Send AT command and wait for response"""
        self.response_buffer = []
        self.waiting_for_response = True
        
        try:
            # Send command
            cmd_bytes = (command + '\r\n').encode('utf-8')
            await self.client.write_gatt_char(self.write_char, cmd_bytes, response=False)
            
            # Wait for response
            await asyncio.sleep(timeout)
            
            # Return collected responses
            return self.response_buffer.copy()
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    async def probe_at_commands(self, category: str = None):
        """Probe all AT commands in a category"""
        categories = [category] if category else self.AT_COMMANDS.keys()
        
        results = {}
        
        for cat in categories:
            print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
            print(f"{Colors.BOLD}[{cat.upper()}] Probing {len(self.AT_COMMANDS[cat])} commands...{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
            
            results[cat] = {}
            
            for cmd in self.AT_COMMANDS[cat]:
                print(f"{Colors.YELLOW}[TX]{Colors.RESET} {cmd:<30}", end=" ", flush=True)
                
                responses = await self.send_at_command(cmd)
                
                if responses:
                    # Filter out empty and echo responses
                    filtered = [r for r in responses if r and r != cmd and r != 'OK' and r != '']
                    
                    if filtered:
                        results[cat][cmd] = filtered
                        print(f"{Colors.GREEN}✓{Colors.RESET}")
                        for resp in filtered[:3]:  # Show first 3 lines
                            print(f"     {Colors.DIM}{resp[:70]}{Colors.RESET}")
                    else:
                        print(f"{Colors.DIM}(no data){Colors.RESET}")
                else:
                    print(f"{Colors.RED}✗{Colors.RESET}")
                
                # Small delay between commands
                await asyncio.sleep(0.3)
        
        return results
    
    async def extract_network_endpoints(self, results: dict) -> dict:
        """Extract UDP/TCP endpoints, IPs, and ports from results"""
        endpoints = {
            'udp_connections': [],
            'tcp_connections': [],
            'local_ip': None,
            'remote_servers': [],
            'pdp_contexts': [],
        }
        
        print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}[NETWORK ANALYSIS] Extracting endpoints...{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
        
        # Parse all responses for network information
        for category, commands in results.items():
            for cmd, responses in commands.items():
                for resp in responses:
                    # Look for IP addresses
                    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                    ips = re.findall(ip_pattern, resp)
                    
                    # Look for ports
                    port_pattern = r':(\d{1,5})\b'
                    ports = re.findall(port_pattern, resp)
                    
                    # CIPOPEN responses (active connections)
                    if 'CIPOPEN' in resp or 'QISTATE' in resp:
                        # Parse connection info
                        if 'UDP' in resp.upper():
                            endpoints['udp_connections'].append({
                                'raw': resp,
                                'ips': ips,
                                'ports': ports
                            })
                        elif 'TCP' in resp.upper():
                            endpoints['tcp_connections'].append({
                                'raw': resp,
                                'ips': ips,
                                'ports': ports
                            })
                    
                    # PDP context info
                    if 'CGDCONT' in resp or 'CGPADDR' in resp:
                        endpoints['pdp_contexts'].append(resp)
                    
                    # Local IP
                    if 'IPADDR' in cmd or 'CGPADDR' in cmd:
                        if ips:
                            endpoints['local_ip'] = ips[0]
                    
                    # Remote servers
                    if ips and 'CIPOPEN' in resp:
                        for ip in ips:
                            if ip not in endpoints['remote_servers']:
                                endpoints['remote_servers'].append(ip)
        
        return endpoints
    
    async def extract_device_identity(self, results: dict) -> dict:
        """Extract device identity information"""
        identity = {
            'imei': None,
            'imsi': None,
            'iccid': None,
            'manufacturer': None,
            'model': None,
            'firmware_version': None,
        }
        
        if 'identity' in results:
            for cmd, responses in results['identity'].items():
                for resp in responses:
                    if 'CGSN' in cmd or 'IMEI' in resp.upper():
                        # Extract IMEI (15 digits)
                        imei_match = re.search(r'\b(\d{15})\b', resp)
                        if imei_match:
                            identity['imei'] = imei_match.group(1)
                    
                    if 'CIMI' in cmd or 'IMSI' in resp.upper():
                        # Extract IMSI (14-15 digits)
                        imsi_match = re.search(r'\b(\d{14,15})\b', resp)
                        if imsi_match:
                            identity['imsi'] = imsi_match.group(1)
                    
                    if 'CCID' in cmd or 'ICCID' in cmd:
                        # Extract ICCID (19-20 digits)
                        iccid_match = re.search(r'\b(\d{19,20})\b', resp)
                        if iccid_match:
                            identity['iccid'] = iccid_match.group(1)
                    
                    if 'CGMI' in cmd:
                        identity['manufacturer'] = resp
                    
                    if 'CGMM' in cmd:
                        identity['model'] = resp
                    
                    if 'CGMR' in cmd or 'VERSION' in cmd.upper():
                        identity['firmware_version'] = resp
        
        return identity
    
    async def run_full_intelligence_scan(self):
        """Run complete intelligence gathering"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    FIRMWARE INTELLIGENCE SCANNER                              ║")
        print("║                   Extracting All Device Information                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        
        # Start notifications
        try:
            await self.client.start_notify(self.notify_char, self.notification_handler)
        except:
            pass
        
        # Probe all AT commands
        results = await self.probe_at_commands()
        
        # Extract structured data
        identity = await self.extract_device_identity(results)
        endpoints = await self.extract_network_endpoints(results)
        
        # Compile intelligence report
        intelligence = {
            'scan_time': datetime.now().isoformat(),
            'device_identity': identity,
            'network_endpoints': endpoints,
            'raw_responses': results
        }
        
        # Print summary
        self.print_intelligence_summary(intelligence)
        
        # Save to file
        self.save_intelligence_report(intelligence)
        
        return intelligence
    
    def print_intelligence_summary(self, intel: dict):
        """Print formatted intelligence summary"""
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}INTELLIGENCE SUMMARY{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        # Device Identity
        print(f"{Colors.CYAN}[DEVICE IDENTITY]{Colors.RESET}")
        identity = intel['device_identity']
        for key, value in identity.items():
            if value:
                print(f"  {key.upper():<20}: {Colors.YELLOW}{value}{Colors.RESET}")
        
        # Network Endpoints
        print(f"\n{Colors.CYAN}[NETWORK ENDPOINTS]{Colors.RESET}")
        endpoints = intel['network_endpoints']
        
        if endpoints['local_ip']:
            print(f"  {'Local IP':<20}: {Colors.YELLOW}{endpoints['local_ip']}{Colors.RESET}")
        
        if endpoints['remote_servers']:
            print(f"  {'Remote Servers':<20}:")
            for server in endpoints['remote_servers']:
                print(f"    {Colors.RED}→ {server}{Colors.RESET}")
        
        if endpoints['udp_connections']:
            print(f"\n  {Colors.BOLD}UDP Connections:{Colors.RESET}")
            for conn in endpoints['udp_connections']:
                print(f"    {Colors.DIM}{conn['raw']}{Colors.RESET}")
        
        if endpoints['tcp_connections']:
            print(f"\n  {Colors.BOLD}TCP Connections:{Colors.RESET}")
            for conn in endpoints['tcp_connections']:
                print(f"    {Colors.DIM}{conn['raw']}{Colors.RESET}")
        
        if endpoints['pdp_contexts']:
            print(f"\n  {Colors.BOLD}PDP Contexts:{Colors.RESET}")
            for ctx in endpoints['pdp_contexts'][:3]:
                print(f"    {Colors.DIM}{ctx}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")
    
    def save_intelligence_report(self, intel: dict):
        """Save intelligence report to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reports/firmware_intelligence_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(intel, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}[SAVED]{Colors.RESET} Intelligence report: {filename}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to save report: {e}")


async def quick_probe_test():
    """Quick test function for development"""
    print("Firmware Intelligence Tool - Test Mode")
    print("This would connect to a real device in production")


if __name__ == "__main__":
    asyncio.run(quick_probe_test())
