"""
Quick verification script to check the latest PDF report
"""

import os
from PyPDF2 import PdfReader

def verify_latest_report():
    reports_dir = "reports"
    
    # Get all R### format PDFs
    pdf_files = [f for f in os.listdir(reports_dir) if f.startswith('R') and f.endswith('.pdf')]
    
    if not pdf_files:
        print("No reports found with R### format")
        return
    
    # Sort and get the latest
    pdf_files.sort()
    latest = pdf_files[-1]
    
    print(f"Latest Report: {latest}")
    print("=" * 60)
    
    # Extract report number from filename
    filename_number = latest.split('_')[0]  # R007
    print(f"Report number from filename: {filename_number}")
    
    # Read PDF and check content
    pdf_path = os.path.join(reports_dir, latest)
    try:
        reader = PdfReader(pdf_path)
        first_page = reader.pages[0]
        text = first_page.extract_text()
        
        # Look for "Report Number:" in the text
        if "Report Number:" in text:
            # Extract the line containing Report Number
            for line in text.split('\n'):
                if "Report Number:" in line:
                    print(f"Report number in PDF: {line.strip()}")
                    break
        
        # Check if they match
        if filename_number in text:
            print(f"\n✅ SUCCESS: Report number matches!")
            print(f"   Filename: {latest}")
            print(f"   Contains: {filename_number}")
        else:
            print(f"\n⚠️  WARNING: Report number might not match")
            
    except Exception as e:
        print(f"Error reading PDF: {e}")
        print("Note: PyPDF2 might not be installed. Install with: pip install PyPDF2")

if __name__ == "__main__":
    verify_latest_report()
