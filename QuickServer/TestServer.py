"""
SENSOR DATA SERVER WITH WEB DASHBOARD
======================================
Receives sensor data via UDP and serves web dashboard
"""

import socket
import datetime
import json
from pathlib import Path
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# Global data storage
sensor_data = {
    'packets': [],
    'latest': {},
    'total_packets': 0
}


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler for dashboard and API"""
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(sensor_data).encode())
            return
        
        elif self.path == '/api/config':
            # Get local IP
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
            except:
                local_ip = "Unknown"
            
            config = {
                'ip': local_ip,
                'port': 8080
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(config).encode())
            return
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass


class SensorDataServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.sock = None
        self.packet_count = 0
        self.log_file = Path('sensor_data_log.txt')
        
    def start(self):
        """Start UDP server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    SENSOR DATA SERVER RUNNING                                 ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[SERVER INFO]{Colors.RESET}")
        print(f"  Listening on: {Colors.YELLOW}{self.host}:{self.port}{Colors.RESET}")
        print(f"  Protocol: {Colors.YELLOW}UDP{Colors.RESET}")
        print(f"  Log file: {Colors.YELLOW}{self.log_file}{Colors.RESET}")
        
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"  Local IP: {Colors.GREEN}{local_ip}{Colors.RESET}")
        except:
            local_ip = "Unknown"
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}READY TO RECEIVE DATA!{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[INSTRUCTIONS]{Colors.RESET}")
        print(f"  1. Use Scanner.py to connect to sensor")
        print(f"  2. Send command: {Colors.CYAN}NB_SHOW{Colors.RESET} (see current server)")
        print(f"  3. Send command: {Colors.CYAN}SET_IP {local_ip}{Colors.RESET}")
        print(f"  4. Send command: {Colors.CYAN}SET_PORT {self.port}{Colors.RESET}")
        print(f"  5. Send command: {Colors.CYAN}TEST_PACKET{Colors.RESET} (test connection)")
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[WAITING FOR DATA...]{Colors.RESET}\n")
        
        # Receive loop
        try:
            while True:
                data, addr = self.sock.recvfrom(4096)
                self.handle_packet(data, addr)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[SHUTDOWN] Server stopped{Colors.RESET}")
            self.sock.close()
    
    def handle_packet(self, data: bytes, addr: tuple):
        """Handle received packet"""
        global sensor_data
        
        self.packet_count += 1
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Print header
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}[PACKET #{self.packet_count}] {timestamp}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}")
        
        # Print source
        print(f"\n{Colors.CYAN}[SOURCE]{Colors.RESET}")
        print(f"  IP: {Colors.YELLOW}{addr[0]}{Colors.RESET}")
        print(f"  Port: {Colors.YELLOW}{addr[1]}{Colors.RESET}")
        
        # Print raw data
        print(f"\n{Colors.CYAN}[RAW DATA]{Colors.RESET}")
        print(f"  Size: {Colors.YELLOW}{len(data)} bytes{Colors.RESET}")
        print(f"  Hex: {Colors.YELLOW}{data.hex()}{Colors.RESET}")
        
        # Try to decode as text
        try:
            text = data.decode('utf-8', errors='ignore')
            if text.strip():
                print(f"  Text: {Colors.YELLOW}{text}{Colors.RESET}")
        except:
            pass
        
        # Parse sensor data (if it matches known format)
        parsed = self.parse_sensor_data(data)
        if parsed:
            print(f"\n{Colors.CYAN}[PARSED DATA]{Colors.RESET}")
            for key, value in parsed.items():
                print(f"  {key}: {Colors.GREEN}{value}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        
        # Store in global data
        packet_info = {
            'timestamp': timestamp,
            'source': f"{addr[0]}:{addr[1]}",
            'hex': data.hex(),
            'parsed': parsed
        }
        sensor_data['packets'].append(packet_info)
        sensor_data['total_packets'] = self.packet_count
        
        # Update latest data
        if parsed:
            sensor_data['latest'] = {
                **sensor_data['latest'],
                **parsed,
                'timestamp': timestamp
            }
        
        # Keep only last 100 packets
        if len(sensor_data['packets']) > 100:
            sensor_data['packets'] = sensor_data['packets'][-100:]
        
        # Log to file
        self.log_packet(timestamp, addr, data, parsed)
    
    def parse_sensor_data(self, data: bytes) -> dict:
        """Try to parse sensor data"""
        try:
            hex_str = data.hex()
            
            # Known packet format from previous analysis
            # Example: 0654351469520520687041006698D6C76590000000000000007
            
            parsed = {}
            
            # Try to extract IMEI (15 digits)
            if len(hex_str) >= 30:
                # IMEI might be in the packet
                for i in range(0, len(hex_str) - 30, 2):
                    chunk = hex_str[i:i+30]
                    try:
                        # Try to decode as BCD
                        imei_candidate = ''.join([chunk[j:j+2] for j in range(0, 30, 2)])
                        if all(c in '0123456789' for c in imei_candidate):
                            parsed['possible_imei'] = imei_candidate
                            break
                    except:
                        pass
            
            # Length
            parsed['packet_length'] = len(data)
            parsed['hex_data'] = hex_str
            
            return parsed if len(parsed) > 2 else None
            
        except Exception as e:
            return None
    
    def log_packet(self, timestamp: str, addr: tuple, data: bytes, parsed: dict):
        """Log packet to file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"[{timestamp}] Packet #{self.packet_count}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Source: {addr[0]}:{addr[1]}\n")
                f.write(f"Size: {len(data)} bytes\n")
                f.write(f"Hex: {data.hex()}\n")
                
                try:
                    text = data.decode('utf-8', errors='ignore')
                    if text.strip():
                        f.write(f"Text: {text}\n")
                except:
                    pass
                
                if parsed:
                    f.write(f"Parsed:\n")
                    for key, value in parsed.items():
                        f.write(f"  {key}: {value}\n")
                
                f.write("\n")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Failed to log: {e}{Colors.RESET}")


if __name__ == "__main__":
    import os
    os.system('')  # Enable ANSI colors on Windows
    
    print(f"\n{Colors.YELLOW}[CONFIG] Starting servers...{Colors.RESET}\n")
    
    # Start HTTP server in background thread
    def start_web_server():
        http_server = HTTPServer(('0.0.0.0', 5000), DashboardHandler)
        print(f"{Colors.GREEN}[WEB] Dashboard running at http://localhost:5000{Colors.RESET}")
        print(f"{Colors.GREEN}[WEB] Open your browser and visit: http://localhost:5000{Colors.RESET}\n")
        http_server.serve_forever()
    
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    # Start UDP server (main thread)
    server = SensorDataServer(host='0.0.0.0', port=8081)
    server.start()

