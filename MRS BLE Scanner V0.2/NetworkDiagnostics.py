"""
Network Diagnostics Module for MRS BLE Scanner V0.2
Analyzes AT command logs and generates PDF diagnostic reports
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DiagnosticResult:
    """Container for diagnostic analysis results"""
    timestamp: str
    device_imei: str
    
    # Layer status
    sim_ready: bool
    imsi: Optional[str]
    imei: Optional[str]
    
    cereg_status: Optional[str]
    cereg_registered: bool
    cereg_code: Optional[str]
    
    netopen_success: bool
    cipopen_success: bool
    cipsend_success: bool
    ack_received: bool
    
    # Signal quality
    rsrp: Optional[int]
    snr: Optional[int]
    rsrp_quality: Optional[str]
    snr_quality: Optional[str]
    
    # Server configuration
    server_ip: Optional[str]
    server_port: Optional[str]
    apn: Optional[str]
    
    # Packet info
    packet_sent: Optional[str]
    packet_bytes: Optional[int]
    
    # Overall status
    overall_status: str  # HEALTHY, PARTIAL, FAILED
    failure_layer: Optional[str]
    root_cause: str
    recommendations: List[str]
    
    # Raw logs
    raw_logs: List[str]


class NetworkDiagnostics:
    """Analyzes NB-IoT network logs and generates diagnostic reports"""
    
    def __init__(self):
        self.log_buffer: List[Tuple[str, str]] = []  # (timestamp, data)
        self.last_test_packet_time = None
        self.analysis_timeout = 15  # seconds after TEST_PACKET to analyze
        
    def add_log(self, timestamp: str, data: str):
        """Add a log entry to the buffer"""
        self.log_buffer.append((timestamp, data))
        
        # Keep only last 500 entries
        if len(self.log_buffer) > 500:
            self.log_buffer = self.log_buffer[-500:]
    
    def detect_test_packet_end(self, data: str) -> bool:
        """
        Detect if TEST_PACKET sequence has ended
        End markers:
        - AT+CIPCLOSE (connection closed)
        - AT+NETCLOSE (network closed)
        - AT+QCSLEEP (going to sleep)
        - AT+CFUN=0 or AT+CFUN=4 (modem off/airplane mode)
        - Multiple CEREG=2,2 in a row (gave up searching)
        """
        end_markers = [
            'AT+CIPCLOSE',
            'AT+NETCLOSE', 
            '+QCSLEEP: HIB2',
            'QCSLEEP=0',
            'AT+CFUN=0',
            'AT+CFUN=4'
        ]
        
        return any(marker in data for marker in end_markers)
    
    def analyze_logs(self, device_imei: str = "Unknown") -> DiagnosticResult:
        """Analyze the log buffer and return diagnostic results"""
        
        # Extract relevant data from logs
        sim_ready = False
        imsi = None
        imei = None
        cereg_status = None
        cereg_registered = False
        cereg_code = None
        netopen_success = False
        cipopen_success = False
        cipsend_success = False
        ack_received = False
        rsrp = None
        snr = None
        packet_sent = None
        packet_bytes = None
        server_ip = None
        server_port = None
        apn = None
        
        # Analyze logs
        for timestamp, data in self.log_buffer:
            # SIM Ready
            if 'SIM Ready' in data:
                sim_ready = True
            
            # IMSI
            imsi_match = re.search(r'AT\+CIMI.*?(\d{15})', data, re.DOTALL)
            if imsi_match:
                imsi = imsi_match.group(1)
            elif re.match(r'^\d{15}$', data.strip()):
                imsi = data.strip()
            
            # IMEI
            imei_match = re.search(r'\+CGSN:\s*"(\d+)"', data)
            if imei_match:
                imei = imei_match.group(1)
            
            # CEREG status
            cereg_match = re.search(r'\+CEREG:\s*(\d+),(\d+)', data)
            if cereg_match:
                mode = cereg_match.group(1)
                status = cereg_match.group(2)
                cereg_code = f"{mode},{status}"
                
                if status == '1' or status == '5':
                    cereg_registered = True
                    cereg_status = "Registered (Home)" if status == '1' else "Registered (Roaming)"
                elif status == '2':
                    cereg_status = "Searching"
                elif status == '3':
                    cereg_status = "Registration Denied"
                elif status == '0':
                    cereg_status = "Not Registered"
            
            # NETOPEN
            if '+NETOPEN: 0' in data or ('AT+NETOPEN' in data and 'OK' in data):
                netopen_success = True
            
            # CIPOPEN
            if '+CIPOPEN: 1,0' in data:
                cipopen_success = True
            
            # CIPSEND
            cipsend_match = re.search(r'\+CIPSEND:\s*1,(\d+),(\d+)', data)
            if cipsend_match:
                requested = int(cipsend_match.group(1))
                sent = int(cipsend_match.group(2))
                if requested == sent:
                    cipsend_success = True
                    packet_bytes = sent
            
            # Packet data
            packet_match = re.search(r'(06\d{48,52})', data)
            if packet_match:
                packet_sent = packet_match.group(1)
            
            # ACK received
            if 'ACK' in data and '+CIPRXGET' in data:
                ack_received = True
            
            # Signal quality
            rsrp_match = re.search(r'RSRP[:\s]+(-?\d+)', data, re.IGNORECASE)
            if rsrp_match:
                rsrp = int(rsrp_match.group(1))
            
            snr_match = re.search(r'SNR[:\s]+(-?\d+)', data, re.IGNORECASE)
            if snr_match:
                snr = int(snr_match.group(1))
            
            # Server IP and Port extraction
            # From CIPOPEN command: AT+CIPOPEN=1,"UDP","47.xxx.xxx.xxx",5000
            cipopen_match = re.search(r'CIPOPEN[^"]*"[^"]*"[^"]*"([^"]+)"[^,]*,(\d+)', data)
            if cipopen_match:
                server_ip = cipopen_match.group(1)
                server_port = cipopen_match.group(2)
            
            # From QIOPEN command: AT+QIOPEN=1,1,"UDP","47.xxx.xxx.xxx",5000
            qiopen_match = re.search(r'QIOPEN[^"]*"[^"]*"[^"]*"([^"]+)"[^,]*,(\d+)', data)
            if qiopen_match:
                server_ip = qiopen_match.group(1)
                server_port = qiopen_match.group(2)
            
            # From NB_SHOW response: Server: 47.xxx.xxx.xxx:8080
            server_match = re.search(r'Server:\s*([0-9.]+):(\d+)', data)
            if server_match:
                server_ip = server_match.group(1)
                server_port = server_match.group(2)
            
            # APN extraction
            # From AT+CGDCONT or AT+QICSGP: "m2mxnbiot"
            apn_match = re.search(r'(?:CGDCONT|QICSGP|APN)[^"]*"([^"]+)"', data, re.IGNORECASE)
            if apn_match:
                apn = apn_match.group(1)
        
        # Determine signal quality
        rsrp_quality = self._evaluate_rsrp(rsrp) if rsrp else None
        snr_quality = self._evaluate_snr(snr) if snr else None
        
        # Determine overall status and failure point
        overall_status, failure_layer, root_cause, recommendations = self._determine_status(
            sim_ready, imsi, cereg_registered, cereg_status, cereg_code,
            netopen_success, cipopen_success, cipsend_success, ack_received,
            rsrp, snr, rsrp_quality, snr_quality
        )
        
        # Use provided IMEI or extracted IMEI
        final_imei = device_imei if device_imei != "Unknown" else (imei or "Unknown")
        
        return DiagnosticResult(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            device_imei=final_imei,
            sim_ready=sim_ready,
            imsi=imsi,
            imei=imei,
            cereg_status=cereg_status,
            cereg_registered=cereg_registered,
            cereg_code=cereg_code,
            netopen_success=netopen_success,
            cipopen_success=cipopen_success,
            cipsend_success=cipsend_success,
            ack_received=ack_received,
            rsrp=rsrp,
            snr=snr,
            rsrp_quality=rsrp_quality,
            snr_quality=snr_quality,
            server_ip=server_ip,
            server_port=server_port,
            apn=apn,
            packet_sent=packet_sent,
            packet_bytes=packet_bytes,
            overall_status=overall_status,
            failure_layer=failure_layer,
            root_cause=root_cause,
            recommendations=recommendations,
            raw_logs=[f"[{ts}] {data}" for ts, data in self.log_buffer[-100:]]
        )
    
    def _evaluate_rsrp(self, rsrp: int) -> str:
        """Evaluate RSRP quality"""
        if rsrp >= -85:
            return "Excellent"
        elif rsrp >= -95:
            return "Good"
        elif rsrp >= -105:
            return "Weak"
        else:
            return "Poor"
    
    def _evaluate_snr(self, snr: int) -> str:
        """Evaluate SNR quality"""
        if snr > 5:
            return "Excellent"
        elif snr >= 0:
            return "Good"
        elif snr >= -5:
            return "Marginal"
        else:
            return "Poor"
    
    def _determine_status(
        self, sim_ready, imsi, cereg_registered, cereg_status, cereg_code,
        netopen_success, cipopen_success, cipsend_success, ack_received,
        rsrp, snr, rsrp_quality, snr_quality
    ) -> Tuple[str, Optional[str], str, List[str]]:
        """
        Determine overall status and provide diagnosis
        Returns: (overall_status, failure_layer, root_cause, recommendations)
        
        SIMPLE LOGIC: If ACK received or data sent successfully = SUCCESS
        Only check SIM/IMSI if device completely failed to communicate
        """
        
        recommendations = []
        
        # ============================================================
        # PRIORITY 1: Check if device successfully communicated
        # ============================================================
        # If ACK received OR data sent successfully, device is working!
        # Don't confuse users with SIM/IMSI checks when device is clearly working
        device_communicated = ack_received or cipsend_success
        
        if device_communicated:
            # Device is working! Skip SIM/IMSI checks entirely
            # Jump directly to checking what level of success we have
            
            if ack_received:
                # Perfect! Full success
                return (
                    "HEALTHY",
                    None,
                    "Device is operating normally - server acknowledged data transmission",
                    ["All systems operating normally", "Data successfully transmitted and acknowledged"]
                )
            elif cipsend_success:
                # Partial success - sent but no ACK
                return (
                    "PARTIAL",
                    "Layer 4: Server Response",
                    "Packet sent successfully but no server acknowledgment received",
                    [
                        "Data was transmitted over NB-IoT network successfully",
                        "Server may not have received packet (UDP is connectionless)",
                        "Check server logs to verify packet arrival",
                        "Verify server is online and responding"
                    ]
                )
        
        # ============================================================
        # PRIORITY 2: Device didn't communicate - now check why
        # ============================================================
        
        # Only check SIM if device completely failed
        if not sim_ready and not cereg_registered:
            return (
                "FAILED",
                "Layer 1: SIM",
                "SIM card not detected or not ready",
                [
                    "Check if SIM card is properly inserted",
                    "Verify SIM card is activated",
                    "Try removing and reinserting SIM card",
                    "Contact carrier to verify SIM status"
                ]
            )
        
        # Layer 2: Registration
        if not cereg_registered:
            if cereg_status == "Searching":
                return (
                    "FAILED",
                    "Layer 2: Registration",
                    f"Modem is searching for network but cannot register (CEREG: {cereg_code})",
                    [
                        "Move device to location with better NB-IoT coverage",
                        "Check if area has NB-IoT network coverage",
                        "Verify SIM is activated for NB-IoT service",
                        "Wait 2-3 minutes for network registration",
                        "Check antenna connection",
                        f"Current signal: RSRP={rsrp}dBm, SNR={snr}dB" if rsrp else "Signal quality unknown"
                    ]
                )
            elif cereg_status == "Registration Denied":
                return (
                    "FAILED",
                    "Layer 2: Registration",
                    f"Network registration denied by carrier (CEREG: {cereg_code})",
                    [
                        "Verify IMEI is whitelisted with carrier",
                        "Check if SIM has active NB-IoT subscription",
                        "Verify APN settings (should be: m2mxnbiot)",
                        "Contact carrier to check account status",
                        f"Device IMEI: {imsi}"
                    ]
                )
            else:
                return (
                    "FAILED",
                    "Layer 2: Registration",
                    f"Not registered to network (CEREG: {cereg_code or 'unknown'})",
                    [
                        "Check network coverage in current location",
                        "Verify SIM card is for NB-IoT network",
                        "Restart device and retry",
                        "Contact carrier support"
                    ]
                )
        
        # Layer 3: PDP Context
        if not netopen_success:
            return (
                "FAILED",
                "Layer 3: PDP Context",
                "Failed to open network PDP context (NETOPEN failed)",
                [
                    "Verify APN configuration: m2mxnbiot",
                    "Check if data service is enabled on SIM",
                    "Network may be temporarily unavailable",
                    "Try sending TEST_PACKET again",
                    f"Registration OK (CEREG: {cereg_code}), but PDP context failed"
                ]
            )
        
        # Layer 4: UDP Socket
        if not cipopen_success:
            return (
                "FAILED",
                "Layer 4: UDP Socket",
                "Failed to open UDP socket (CIPOPEN failed)",
                [
                    "Network context is open but socket creation failed",
                    "Server may be unreachable",
                    "Check firewall settings on server side",
                    "Verify UDP port 5000 is accessible",
                    "Try sending TEST_PACKET again"
                ]
            )
        
        if not cipsend_success:
            return (
                "FAILED",
                "Layer 4: Data Transmission",
                "Failed to send data packet (CIPSEND failed)",
                [
                    "Socket is open but data transmission failed",
                    "Network connection may be unstable",
                    "Check signal quality",
                    f"Signal: RSRP={rsrp}dBm ({rsrp_quality}), SNR={snr}dB ({snr_quality})" if rsrp else "Check signal strength",
                    "Retry transmission"
                ]
            )
        
        # Check ACK
        if not ack_received:
            return (
                "PARTIAL",
                "Layer 4: Server Response",
                "Packet sent successfully but no ACK received from server",
                [
                    "Data was transmitted over NB-IoT network",
                    "Server may not have received the packet (UDP is connectionless)",
                    "Server may be offline or not responding",
                    "Check server logs to verify packet arrival",
                    "This is normal for UDP - no delivery guarantee",
                    f"Packet sent: {packet_bytes} bytes" if packet_bytes else "Packet transmitted"
                ]
            )
        
        # Check signal quality for warnings
        if rsrp and rsrp < -105:
            recommendations.append(f"⚠️ Weak signal: RSRP={rsrp}dBm ({rsrp_quality})")
        if snr and snr < 0:
            recommendations.append(f"⚠️ Poor SNR: {snr}dB ({snr_quality})")
        
        if not recommendations:
            recommendations = [
                "✅ All systems operating normally",
                "Device successfully registered and transmitted data",
                "Server acknowledged packet receipt",
                f"Signal quality: RSRP={rsrp}dBm ({rsrp_quality}), SNR={snr}dB ({snr_quality})" if rsrp else "Signal quality good"
            ]
        
        # All checks passed
        return (
            "HEALTHY",
            None,
            "Device is operating normally. All layers functional.",
            recommendations
        )
    
    def clear_logs(self):
        """Clear the log buffer"""
        self.log_buffer.clear()
