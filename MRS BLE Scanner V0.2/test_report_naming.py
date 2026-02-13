"""
Test script to verify the new report naming and numbering system
"""

from PDFReportGenerator import PDFReportGenerator
from NetworkDiagnostics import DiagnosticResult
from datetime import datetime
import os

def create_test_result():
    """Create a sample diagnostic result for testing"""
    return DiagnosticResult(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        device_imei="351469520520687",
        sim_ready=True,
        imsi="502153123456789",
        imei="351469520520687",
        cereg_status="Registered (home network)",
        cereg_registered=True,
        cereg_code="1",
        netopen_success=True,
        cipopen_success=True,
        cipsend_success=True,
        ack_received=True,
        rsrp=-85,
        rsrp_quality="Good",
        snr=10,
        snr_quality="Excellent",
        server_ip="47.254.129.55",
        server_port="5005",
        apn="nb.iot",
        packet_sent="48656C6C6F",
        packet_bytes=100,
        overall_status="HEALTHY",
        failure_layer=None,
        root_cause="Device is operating normally",
        recommendations=["System is operating normally"],
        raw_logs=["[12:00:00] Test log entry"]
    )

def test_report_generation():
    """Test the new report naming and numbering system"""
    print("=" * 80)
    print("TESTING NEW REPORT NAMING & NUMBERING SYSTEM")
    print("=" * 80)
    
    # Initialize PDF generator
    pdf_gen = PDFReportGenerator()
    
    # Check current counter
    counter_file = pdf_gen.counter_file
    print(f"\nCounter file: {counter_file}")
    
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            current_count = f.read().strip()
        print(f"Current counter value: {current_count}")
    else:
        print("Counter file doesn't exist yet (will start at 1)")
    
    # Generate 3 test reports
    print("\n" + "=" * 80)
    print("GENERATING 3 TEST REPORTS")
    print("=" * 80)
    
    result = create_test_result()
    
    for i in range(3):
        print(f"\n[Test {i+1}] Generating report...")
        pdf_path = pdf_gen.generate_report(result)
        print(f"✓ Generated: {os.path.basename(pdf_path)}")
    
    # Check final counter value
    print("\n" + "=" * 80)
    print("FINAL COUNTER VALUE")
    print("=" * 80)
    
    with open(counter_file, 'r') as f:
        final_count = f.read().strip()
    print(f"Counter after 3 reports: {final_count}")
    
    # List all reports
    print("\n" + "=" * 80)
    print("ALL REPORTS IN DIRECTORY")
    print("=" * 80)
    
    reports_dir = pdf_gen.output_dir
    files = sorted([f for f in os.listdir(reports_dir) if f.endswith('.pdf')])
    
    print(f"\nFound {len(files)} PDF reports:")
    for f in files:
        print(f"  • {f}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\nExpected behavior:")
    print("  ✓ Filenames should be: R001_YYYYMMDD_HHMMSS.pdf")
    print("  ✓ Report numbers should increment across multiple runs")
    print("  ✓ Counter file should persist between runs")
    print("\nVerify:")
    print("  1. Check that new reports use the R### format")
    print("  2. Run this script again to verify counter increments")
    print("  3. Check that report numbers in PDF match filenames")

if __name__ == "__main__":
    test_report_generation()
