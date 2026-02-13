"""
CUSTOM PROTOCOL ANALYZER
========================
Reverse engineer the sensor's custom protocol by:
1. Brute forcing all possible commands
2. Analyzing response patterns
3. Mapping the complete command set
4. Finding configuration interface
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


class CustomProtocolAnalyzer:
    """Analyze custom sensor protocol"""
    
    # Command patterns to try
    COMMAND_PATTERNS = {
        'ati_variants': [f'ATI{i}' for i in range(100)],  # ATI0-ATI99
        
        'at_variants': [
            'AT', 'AT?', 'AT!', 'AT#',
            'ATE0', 'ATE1', 'ATV0', 'ATV1',
            'AT&F', 'AT&V', 'AT&W', 'ATZ',
        ],
        
        'config_commands': [
            'CONFIG', 'CONFIG?', 'SETCONFIG',
            'GETCONFIG', 'SHOWCONFIG', 'LISTCONFIG',
            'SET', 'GET', 'SHOW', 'LIST',
        ],
        
        'server_commands': [
            'SERVER', 'SERVER?', 'SETSERVER', 'GETSERVER',
            'HOST', 'HOST?', 'SETHOST', 'GETHOST',
            'IP', 'IP?', 'SETIP', 'GETIP',
            'PORT', 'PORT?', 'SETPORT', 'GETPORT',
            'URL', 'URL?', 'SETURL', 'GETURL',
        ],
        
        'network_commands': [
            'NETWORK', 'NETWORK?', 'NET', 'NET?',
            'APN', 'APN?', 'SETAPN', 'GETAPN',
            'CONNECT', 'DISCONNECT', 'STATUS',
            'SIGNAL', 'RSSI', 'IMEI', 'IMSI',
        ],
        
        'sensor_commands': [
            'SENSOR', 'SENSOR?', 'SENSORS',
            'READ', 'MEASURE', 'DATA',
            'DISTANCE', 'ANGLE', 'IMU',
            'CALIBRATE', 'RESET', 'ZERO',
        ],
        
        'firmware_commands': [
            'VERSION', 'VER', 'FW', 'FIRMWARE',
            'UPDATE', 'UPGRADE', 'FLASH',
            'BOOTLOADER', 'BOOT', 'DFU',
            'DUMP', 'READ', 'WRITE',
        ],
        
        'debug_commands': [
            'DEBUG', 'DEBUG?', 'LOG', 'TRACE',
            'VERBOSE', 'QUIET', 'ECHO',
            'TEST', 'DIAG', 'DIAGNOSTIC',
        ],
        
        'help_commands': [
            'HELP', 'HELP?', '?', 'COMMANDS',
            'INFO', 'ABOUT', 'MANUAL',
        ],
        
        'memory_commands': [
            'MEM', 'MEMORY', 'DUMP', 'READ',
            'FLASH', 'EEPROM', 'RAM',
        ],
        
        'special_chars': [
            '\r', '\n', '\r\n',
            '+++', '---', '***',
            'ESC', 'CTRL+C', 'CTRL+Z',
        ],
    }
    
    def __init__(self, client: BleakClient, write_char_uuid: str, notify_char_uuid: str):
        self.client = client
        self.write_char = write_char_uuid
        self.notify_char = notify_char_uuid
        self.response_buffer = []
        self.discovered_commands = {}
        
    def notification_handler(self, sender, data):
        """Capture all responses"""
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
    
    async def send_command(self, command: str, timeout: float = 2.0) -> dict:
        """Send command and capture response"""
        self.response_buffer = []
        start_time = time.time()
        
        try:
            # Try different line endings
            for ending in ['\r\n', '\n', '\r', '']:
                cmd_bytes = (command + ending).encode('utf-8')
                await self.client.write_gatt_char(self.write_char, cmd_bytes, response=False)
                await asyncio.sleep(0.1)
            
            # Wait for response
            await asyncio.sleep(timeout)
            
            end_time = time.time()
            
            # Filter out echo
            responses = [r for r in self.response_buffer if r['data'] != command]
            
            return {
                'command': command,
                'responses': responses,
                'response_time': end_time - start_time,
                'success': len(responses) > 0
            }
            
        except Exception as e:
            return {
                'command': command,
                'error': str(e),
                'success': False
            }
    
    async def brute_force_commands(self):
        """Try all possible command variations"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    CUSTOM PROTOCOL ANALYZER                                   ║")
        print("║                    Brute Force Command Discovery                              ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        
        total_commands = sum(len(cmds) for cmds in self.COMMAND_PATTERNS.values())
        current = 0
        
        for category, commands in self.COMMAND_PATTERNS.items():
            print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
            print(f"{Colors.BOLD}[{category.upper()}] Testing {len(commands)} commands...{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
            
            for cmd in commands:
                current += 1
                progress = (current / total_commands) * 100
                
                print(f"{Colors.DIM}[{current}/{total_commands}] {progress:5.1f}%{Colors.RESET} ", end="")
                print(f"{Colors.YELLOW}[TX]{Colors.RESET} {cmd:<30}", end=" ", flush=True)
                
                result = await self.send_command(cmd, timeout=2.0)
                
                if result['success'] and len(result['responses']) > 0:
                    # Found a working command!
                    self.discovered_commands[cmd] = result
                    print(f"{Colors.GREEN}✓ ({len(result['responses'])} responses){Colors.RESET}")
                    
                    # Show response preview
                    for resp in result['responses'][:2]:  # Show first 2 responses
                        preview = resp['data'][:70]
                        print(f"     {Colors.GREEN}→{Colors.RESET} {preview}")
                else:
                    print(f"{Colors.DIM}✗{Colors.RESET}")
                
                # Small delay to not overwhelm device
                await asyncio.sleep(0.1)
        
        return self.discovered_commands
    
    def analyze_responses(self, commands: dict) -> dict:
        """Analyze response patterns"""
        analysis = {
            'total_working_commands': len(commands),
            'response_patterns': {},
            'data_types': {
                'sensor_data': [],
                'imu_data': [],
                'state_changes': [],
                'configuration': [],
                'unknown': []
            }
        }
        
        for cmd, result in commands.items():
            for resp in result['responses']:
                data = resp['data']
                
                # Classify response type
                if 's1:' in data or 's2:' in data:
                    analysis['data_types']['sensor_data'].append({
                        'command': cmd,
                        'data': data
                    })
                elif 'angle' in data or 'x=' in data:
                    analysis['data_types']['imu_data'].append({
                        'command': cmd,
                        'data': data
                    })
                elif 'Open' in data or 'Close' in data:
                    analysis['data_types']['state_changes'].append({
                        'command': cmd,
                        'data': data
                    })
                elif 'distance:' in data:
                    analysis['data_types']['sensor_data'].append({
                        'command': cmd,
                        'data': data
                    })
                else:
                    analysis['data_types']['unknown'].append({
                        'command': cmd,
                        'data': data
                    })
        
        return analysis
    
    def save_protocol_map(self, commands: dict, analysis: dict):
        """Save complete protocol map"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reports/protocol_map_{timestamp}.json"
        
        report = {
            'extraction_time': datetime.now().isoformat(),
            'discovered_commands': commands,
            'analysis': analysis,
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n{Colors.GREEN}[SAVED]{Colors.RESET} Protocol map: {filename}")
            return filename
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Failed to save: {e}")
            return None
    
    async def run_protocol_analysis(self):
        """Run complete protocol analysis"""
        # Start notifications
        try:
            await self.client.start_notify(self.notify_char, self.notification_handler)
        except:
            pass
        
        # Brute force commands
        commands = await self.brute_force_commands()
        
        # Analyze responses
        print(f"\n{Colors.YELLOW}[ANALYZING] Response patterns...{Colors.RESET}")
        analysis = self.analyze_responses(commands)
        
        # Save report
        report_file = self.save_protocol_map(commands, analysis)
        
        # Print summary
        self.print_summary(commands, analysis)
        
        return commands, analysis, report_file
    
    def print_summary(self, commands: dict, analysis: dict):
        """Print analysis summary"""
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}PROTOCOL ANALYSIS SUMMARY{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[DISCOVERED COMMANDS]{Colors.RESET}")
        print(f"  Total Working Commands: {len(commands)}")
        
        print(f"\n{Colors.CYAN}[DATA TYPES]{Colors.RESET}")
        for dtype, items in analysis['data_types'].items():
            if items:
                print(f"  {dtype.replace('_', ' ').title():<20}: {len(items)} responses")
        
        print(f"\n{Colors.CYAN}[WORKING COMMANDS]{Colors.RESET}")
        for cmd in sorted(commands.keys()):
            print(f"  {Colors.GREEN}✓{Colors.RESET} {cmd}")
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")


if __name__ == "__main__":
    print("Custom Protocol Analyzer - Use via ProtocolCracker.py")
