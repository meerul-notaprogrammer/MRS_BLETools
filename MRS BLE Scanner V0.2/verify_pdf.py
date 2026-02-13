"""
Verify Server Config in PDF
"""
import PyPDF2
import sys

pdf_path = "reports/Network_Report_162464_20260213_175948_#999.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        print("=" * 80)
        print("PDF CONTENT VERIFICATION")
        print("=" * 80)
        print()
        
        # Check for server configuration section
        if "Server Configuration" in text:
            print("✅ 'Server Configuration' section FOUND!")
        else:
            print("❌ 'Server Configuration' section NOT FOUND")
        
        if "47.245.56.17" in text:
            print("✅ Server IP '47.245.56.17' FOUND!")
        else:
            print("❌ Server IP NOT FOUND")
        
        if "8080" in text:
            print("✅ Server Port '8080' FOUND!")
        else:
            print("❌ Server Port NOT FOUND")
        
        if "m2mxnbiot" in text:
            print("✅ APN 'm2mxnbiot' FOUND!")
        else:
            print("❌ APN NOT FOUND")
        
        print()
        print("=" * 80)
        print("EXTRACTED TEXT PREVIEW:")
        print("=" * 80)
        
        # Find and print server config section
        if "Server Configuration" in text:
            start = text.find("Server Configuration")
            end = start + 200
            print(text[start:end])
        
except ImportError:
    print("PyPDF2 not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPDF2', '-q'])
    print("Please run this script again.")
except Exception as e:
    print(f"Error: {e}")
