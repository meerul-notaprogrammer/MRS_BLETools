"""
DEEP FIRMWARE EXTRACTOR
=======================
Advanced extraction tool to get EVERYTHING from the sensor:
- Kernel information
- Complete AT command set discovery
- Memory dumps (if accessible)
- Configuration files
- Bootloader info
- Hardware capabilities
- Protocol analysis
- Timing analysis
"""

import asyncio
import re
from datetime import datetime
from bleak import BleakClient
import json
import time


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


class DeepFirmwareExtractor:
    """Deep extraction of ALL firmware information"""
    
    # Comprehensive AT command discovery
    AT_COMMANDS_DEEP = {
        # System & Kernel Info
        'system': [
            'ATI',              # Device info
            'ATI0', 'ATI1', 'ATI2', 'ATI3', 'ATI4', 'ATI5', 'ATI6', 'ATI7', 'ATI8', 'ATI9',
            'AT+GMI',           # Manufacturer
            'AT+GMM',           # Model
            'AT+GMR',           # Revision
            'AT+GSN',           # Serial number
            'AT+CGMI',          # Manufacturer ID
            'AT+CGMM',          # Model ID
            'AT+CGMR',          # Firmware revision
            'AT+CGSN',          # IMEI
            'AT+CGSN=1',        # IMEI with type
            'AT+CIMI',          # IMSI
            'AT+CCID',          # ICCID
            'AT+ICCID',         # ICCID alternative
            'AT+QCCID',         # Quectel ICCID
        ],
        
        # Bootloader & Firmware
        'bootloader': [
            'AT+QFOTADL?',      # Firmware download status
            'AT+QFOTASTAT?',    # FOTA status
            'AT+QVERSION',      # Firmware version
            'AT+QHWVER',        # Hardware version
            'AT+QSUBSYSVER',    # Subsystem version
            'AT+QMBNCFG?',      # MBN configuration
            'AT+QCFG="firmware"',  # Firmware config
        ],
        
        # Memory & Storage
        'memory': [
            'AT+QFLDS',         # List files
            'AT+QFLST',         # File list
            'AT+QFUPL?',        # File upload status
            'AT+QFDWL?',        # File download status
            'AT+QFOPEN?',       # Open files
            'AT+QFLDS="*"',     # List all files
        ],
        
        # Network Configuration (Deep)
        'network_deep': [
            'AT+CGDCONT?',      # PDP context
            'AT+CGACT?',        # PDP activation
            'AT+CGPADDR',       # PDP addresses
            'AT+CGCONTRDP',     # Dynamic PDP context
            'AT+COPS?',         # Operator selection
            'AT+COPS=?',        # Available operators (slow!)
            'AT+CREG?',         # Network registration
            'AT+CGREG?',        # GPRS registration
            'AT+CEREG?',        # EPS registration
            'AT+CEREG=2',       # Enable detailed registration
            'AT+QNWINFO',       # Network info
            'AT+QENG="servingcell"',  # Serving cell
            'AT+QENG="neighbourcell"', # Neighbor cells
            'AT+QSPN',          # Service provider name
        ],
        
        # Socket & Connection (Deep)
        'socket_deep': [
            'AT+NETOPEN?',      # Network status
            'AT+CIPOPEN?',      # Socket status
            'AT+CIPSTATUS',     # Connection status
            'AT+CIPSHOW?',      # Show remote IP
            'AT+CIPSHOW=1',     # Enable show remote
            'AT+NETSTAT',       # Network statistics
            'AT+QISTATE',       # Query socket state
            'AT+QISTATE=1,1',   # Query specific socket
            'AT+QIACT?',        # Query PDP context
            'AT+QICFG?',        # Socket configuration
        ],
        
        # Signal & RF (Deep)
        'signal_deep': [
            'AT+CSQ',           # Signal quality
            'AT+QCSQ',          # Extended signal quality
            'AT+QNWINFO',       # Network info
            'AT+QENG="servingcell"',  # Cell info
            'AT+QCBCINFOSC',    # Cell info with RSRP/SNR
            'AT+QNBIOTEVENT?',  # NB-IoT events
            'AT+QCSTATUS?',     # Query status
            'AT+QCFG="band"',   # Band configuration
            'AT+QCFG="nwscanmode"',  # Scan mode
            'AT+QCFG="iotopmode"',   # IoT mode
            'AT+QCFG="servicedomain"', # Service domain
        ],
        
        # Power & Sleep (Deep)
        'power_deep': [
            'AT+QCSLEEP?',      # Sleep mode
            'AT+QSCLK?',        # Sleep clock
            'AT+CPSMS?',        # Power saving mode
            'AT+CPSMS=?',       # PSM capabilities
            'AT+CEDRXS?',       # eDRX settings
            'AT+CEDRXS=?',      # eDRX capabilities
            'AT+QCFG="psm/enter"',  # PSM entry
            'AT+QCFG="psm/urc"',    # PSM URC
            'AT+QPOWD?',        # Power down
        ],
        
        # Configuration (Deep)
        'config_deep': [
            'AT&V',             # Display config
            'AT&V0', 'AT&V1',   # Config profiles
            'AT+QCFG=?',        # List all configs
            'AT+QCFG="list"',   # Config list
            'AT+CMEE?',         # Error reporting
            'AT+CMEE=2',        # Enable verbose errors
            'AT+QURCCFG?',      # URC configuration
            'AT+QINDCFG?',      # Indication config
        ],
        
        # GPIO & Hardware
        'hardware': [
            'AT+QGPIO?',        # GPIO status
            'AT+QADC?',         # ADC reading
            'AT+QTEMP',         # Temperature
            'AT+QPOWD?',        # Power status
            'AT+CBC',           # Battery charge
            'AT+QPSMEXTCFG?',   # PSM extended config
        ],
        
        # SIM & Security
        'sim_security': [
            'AT+CPIN?',         # SIM PIN status
            'AT+CLCK=?',        # Facility lock capabilities
            'AT+CPWD=?',        # Password capabilities
            'AT+CRSM=?',        # Restricted SIM access
            'AT+CSIM=?',        # Generic SIM access
        ],
        
        # Vendor Specific (Quectel)
        'vendor_quectel': [
            'AT+QVERSION',      # Version info
            'AT+QHWVER',        # Hardware version
            'AT+QSUBSYSVER',    # Subsystem version
            'AT+QGMR',          # Firmware revision
            'AT+QDEVINFO',      # Device info
            'AT+QCFG="apready"',  # Application ready
            'AT+QCFG="urc/ri/ring"',  # Ring URC
            'AT+QCFG="urc/ri/smsincoming"',  # SMS URC
            'AT+QCFG="urc/delay"',  # URC delay
        ],
        
        # Protocol Discovery
        'protocol_discovery': [
            'AT+QIURC',         # URC mode
            'AT+QISDE?',        # Data encoding
            'AT+QICSGP?',       # Set CSD or GPRS
            'AT+QIDNSCFG?',     # DNS configuration
            'AT+QIDNSGIP?',     # DNS query
        ],
        
        # Timing & Sync
        'timing': [
            'AT+CCLK?',         # Clock
            'AT+QLTS?',         # Local time stamp
            'AT+QNITZ?',        # Network time
        ],
    }
    
    # Brute force AT command discovery
    AT_COMMAND_PATTERNS = [
        'AT+Q{}',           # Quectel commands
        'AT+C{}',           # Standard commands
        'AT+{}',            # Generic
        'AT#{}',            # Alternative prefix
        'AT${}',            # Alternative prefix
        'AT%{}',            # Alternative prefix
    ]
    
    def __init__(self, client: BleakClient, write_char_uuid: str, notify_char_uuid: str):
        self.client = client
        self.write_char = write_char_uuid
        self.notify_char = notify_char_uuid
        self.response_buffer = []
        self.all_responses = {}
        self.discovered_commands = []
        self.timing_data = {}
        
    def notification_handler(self, sender, data):
        """Capture all responses with timing"""
        if data:
            try:
                text = data.decode('utf-8', errors='ignore').strip()
                if text:
                    self.response_buffer.append({
                        'timestamp': time.time(),
                        'data': text,
                        'hex': data.hex()
                    })
            except:
                pass
    
    async def send_at_command(self, command: str, timeout: float = 3.0) -> dict:
        """Send AT command and capture detailed response"""
        self.response_buffer = []
        start_time = time.time()
        
        try:
            # Send command
            cmd_bytes = (command + '\r\n').encode('utf-8')
            await self.client.write_gatt_char(self.write_char, cmd_bytes, response=False)
            
            # Wait for response
            await asyncio.sleep(timeout)
            
            end_time = time.time()
            
            return {
                'command': command,
                'responses': self.response_buffer.copy(),
                'response_time': end_time - start_time,
                'response_count': len(self.response_buffer),
                'success': len(self.response_buffer) > 0
            }
            
        except Exception as e:
            return {
                'command': command,
                'error': str(e),
                'success': False
            }
    
    async def deep_probe_all_commands(self):
        """Probe ALL AT commands comprehensively"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    DEEP FIRMWARE EXTRACTION                                   ║")
        print("║                    Probing ALL AT Commands                                    ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        
        total_commands = sum(len(cmds) for cmds in self.AT_COMMANDS_DEEP.values())
        current = 0
        
        for category, commands in self.AT_COMMANDS_DEEP.items():
            print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
            print(f"{Colors.BOLD}[{category.upper()}] Probing {len(commands)} commands...{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
            
            self.all_responses[category] = {}
            
            for cmd in commands:
                current += 1
                progress = (current / total_commands) * 100
                
                print(f"{Colors.DIM}[{current}/{total_commands}] {progress:5.1f}%{Colors.RESET} ", end="")
                print(f"{Colors.YELLOW}[TX]{Colors.RESET} {cmd:<35}", end=" ", flush=True)
                
                result = await self.send_at_command(cmd, timeout=4.0)
                
                if result['success'] and result['response_count'] > 0:
                    # Filter meaningful responses
                    meaningful = [r for r in result['responses'] 
                                 if r['data'] and r['data'] != cmd and r['data'] != 'OK']
                    
                    if meaningful:
                        self.all_responses[category][cmd] = result
                        self.discovered_commands.append(cmd)
                        print(f"{Colors.GREEN}✓ ({len(meaningful)} lines){Colors.RESET}")
                        
                        # Show first response
                        if meaningful:
                            preview = meaningful[0]['data'][:60]
                            print(f"     {Colors.DIM}{preview}{Colors.RESET}")
                    else:
                        print(f"{Colors.DIM}(OK only){Colors.RESET}")
                else:
                    print(f"{Colors.RED}✗{Colors.RESET}")
                
                # Small delay
                await asyncio.sleep(0.2)
        
        return self.all_responses
    
    async def extract_kernel_info(self, responses: dict) -> dict:
        """Extract kernel and system information"""
        kernel_info = {
            'firmware_version': None,
            'hardware_version': None,
            'bootloader_version': None,
            'kernel_version': None,
            'subsystem_versions': [],
            'build_date': None,
            'build_id': None,
        }
        
        # Parse system responses
        if 'system' in responses:
            for cmd, result in responses['system'].items():
                for resp in result.get('responses', []):
                    data = resp['data']
                    
                    # Look for version patterns
                    if 'Revision' in data or 'VERSION' in data.upper():
                        kernel_info['firmware_version'] = data
                    
                    # Look for build dates
                    date_match = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', data)
                    if date_match:
                        kernel_info['build_date'] = date_match.group(0)
        
        # Parse bootloader info
        if 'bootloader' in responses:
            for cmd, result in responses['bootloader'].items():
                for resp in result.get('responses', []):
                    data = resp['data']
                    
                    if 'QVERSION' in cmd:
                        kernel_info['kernel_version'] = data
                    elif 'QHWVER' in cmd:
                        kernel_info['hardware_version'] = data
                    elif 'QSUBSYSVER' in cmd:
                        kernel_info['subsystem_versions'].append(data)
        
        return kernel_info
    
    async def extract_complete_network_config(self, responses: dict) -> dict:
        """Extract complete network configuration"""
        network_config = {
            'pdp_contexts': [],
            'active_connections': [],
            'dns_servers': [],
            'routing_table': [],
            'apn_settings': {},
            'operator_info': {},
        }
        
        # Parse network responses
        for category in ['network_deep', 'socket_deep']:
            if category in responses:
                for cmd, result in responses[category].items():
                    for resp in result.get('responses', []):
                        data = resp['data']
                        
                        # PDP contexts
                        if 'CGDCONT' in data:
                            network_config['pdp_contexts'].append(data)
                        
                        # Active connections
                        if 'CIPOPEN' in data or 'QISTATE' in data:
                            network_config['active_connections'].append(data)
                        
                        # Operator info
                        if 'COPS' in data:
                            network_config['operator_info']['raw'] = data
        
        return network_config
    
    def save_deep_extraction_report(self, data: dict):
        """Save comprehensive extraction report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reports/deep_extraction_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n{Colors.GREEN}[SAVED]{Colors.RESET} Deep extraction report: {filename}")
            return filename
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Failed to save: {e}")
            return None
    
    async def run_deep_extraction(self):
        """Run complete deep extraction"""
        # Start notifications
        try:
            await self.client.start_notify(self.notify_char, self.notification_handler)
        except:
            pass
        
        # Probe all commands
        responses = await self.deep_probe_all_commands()
        
        # Extract structured intelligence
        print(f"\n{Colors.YELLOW}[ANALYZING] Extracting structured intelligence...{Colors.RESET}")
        
        kernel_info = await self.extract_kernel_info(responses)
        network_config = await self.extract_complete_network_config(responses)
        
        # Compile complete report
        deep_extraction = {
            'extraction_time': datetime.now().isoformat(),
            'total_commands_probed': sum(len(cmds) for cmds in self.AT_COMMANDS_DEEP.values()),
            'successful_commands': len(self.discovered_commands),
            'discovered_commands': self.discovered_commands,
            'kernel_info': kernel_info,
            'network_config': network_config,
            'raw_responses': responses,
        }
        
        # Save report
        report_file = self.save_deep_extraction_report(deep_extraction)
        
        # Print summary
        self.print_deep_summary(deep_extraction)
        
        return deep_extraction, report_file
    
    def print_deep_summary(self, data: dict):
        """Print comprehensive summary"""
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}DEEP EXTRACTION SUMMARY{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[STATISTICS]{Colors.RESET}")
        print(f"  Total Commands Probed : {data['total_commands_probed']}")
        print(f"  Successful Responses  : {data['successful_commands']}")
        print(f"  Success Rate          : {(data['successful_commands']/data['total_commands_probed']*100):.1f}%")
        
        print(f"\n{Colors.CYAN}[KERNEL INFORMATION]{Colors.RESET}")
        kernel = data['kernel_info']
        for key, value in kernel.items():
            if value:
                print(f"  {key.replace('_', ' ').title():<20}: {Colors.YELLOW}{value}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[DISCOVERED COMMANDS]{Colors.RESET}")
        print(f"  {Colors.GREEN}{len(data['discovered_commands'])} working AT commands found{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")


if __name__ == "__main__":
    print("Deep Firmware Extractor - Use via CrackFirmware_Deep.py")
