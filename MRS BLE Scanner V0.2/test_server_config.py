"""
Test Server Configuration Extraction
=====================================
Simulates sensor data to test if server IP/port extraction works
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from NetworkDiagnostics import NetworkDiagnostics
from PDFReportGenerator import PDFReportGenerator

print("=" * 80)
print("TESTING SERVER CONFIGURATION EXTRACTION")
print("=" * 80)
print()

# Create diagnostics instance
diagnostics = NetworkDiagnostics()

# Simulate log data with server configuration
print("[1] Adding simulated NB_SHOW response...")
diagnostics.add_log("2026-02-13 17:59:00", "NB_SHOW")
diagnostics.add_log("2026-02-13 17:59:01", "Server: 47.245.56.17:8080")
diagnostics.add_log("2026-02-13 17:59:01", "APN: m2mxnbiot")
diagnostics.add_log("2026-02-13 17:59:01", "Status: Connected")
print("   ✓ Added NB_SHOW response")
print()

# Simulate AT commands with server info
print("[2] Adding simulated AT commands...")
diagnostics.add_log("2026-02-13 17:59:02", 'AT+CIPOPEN=1,"UDP","47.245.56.17",8080')
diagnostics.add_log("2026-02-13 17:59:03", "+CIPOPEN: 1,0")
diagnostics.add_log("2026-02-13 17:59:04", 'AT+CGDCONT=1,"IP","m2mxnbiot"')
print("   ✓ Added AT commands")
print()

# Simulate successful transmission
print("[3] Adding simulated successful transmission...")
diagnostics.add_log("2026-02-13 17:59:05", "SIM Ready")
diagnostics.add_log("2026-02-13 17:59:06", "+CEREG: 2,1")
diagnostics.add_log("2026-02-13 17:59:07", "+NETOPEN: 0")
diagnostics.add_log("2026-02-13 17:59:08", "+CIPSEND: 1,50,50")
diagnostics.add_log("2026-02-13 17:59:09", "065435146952052068704100669")
diagnostics.add_log("2026-02-13 17:59:10", "RSRP: -95")
diagnostics.add_log("2026-02-13 17:59:11", "SNR: 3")
print("   ✓ Added transmission logs")
print()

# Analyze logs
print("[4] Analyzing logs...")
result = diagnostics.analyze_logs(device_imei="351469520162464")
print("   ✓ Analysis complete")
print()

# Display results
print("=" * 80)
print("EXTRACTION RESULTS")
print("=" * 80)
print()

print(f"Device IMEI:     {result.device_imei}")
print(f"Overall Status:  {result.overall_status}")
print()

print("SERVER CONFIGURATION:")
print(f"  Server IP:     {result.server_ip or 'NOT FOUND'}")
print(f"  Server Port:   {result.server_port or 'NOT FOUND'}")
print(f"  APN:           {result.apn or 'NOT FOUND'}")
print()

print("NETWORK STATUS:")
print(f"  SIM Ready:     {result.sim_ready}")
print(f"  Registered:    {result.cereg_registered}")
print(f"  Data Sent:     {result.cipsend_success}")
print(f"  RSRP:          {result.rsrp} dBm ({result.rsrp_quality})")
print(f"  SNR:           {result.snr} dB ({result.snr_quality})")
print()

# Generate PDF report
print("[5] Generating PDF report...")
pdf_gen = PDFReportGenerator(output_dir="reports")
report_path = pdf_gen.generate_report(result, report_number=999)
print(f"   ✓ Report generated: {report_path}")
print()

# Verify server config was extracted
print("=" * 80)
print("VERIFICATION")
print("=" * 80)
print()

if result.server_ip and result.server_port:
    print("✅ SUCCESS! Server configuration extracted:")
    print(f"   Server: {result.server_ip}:{result.server_port}")
    print(f"   APN: {result.apn}")
    print()
    print("✅ PDF report should contain 'Server Configuration' section")
    print(f"   Open: {report_path}")
else:
    print("❌ FAILED! Server configuration NOT extracted")
    print("   Check the regex patterns in NetworkDiagnostics.py")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
