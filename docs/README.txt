MRS BLE Scanner Tool V0.2.0
Professional Scan, Read, Command, Diagnose using BLE, HTTP and Auto PDF Reports

🆕 NEW IN V0.2
- ✅ Automatic network diagnostics after every TEST_PACKET
- ✅ Professional PDF reports with layer-by-layer analysis
- ✅ Root cause identification and actionable recommendations
- ✅ Signal quality evaluation (RSRP/SNR)
- ✅ Report history with timestamps
- ✅ Manual report generation on-demand

Requirements
- Windows 10/11
- Python 3.8+ (auto-installed if missing)

Quick Start
1. Open Start.bat
2. Answer User Agreement
3. Enter API URL (or press ENTER to skip)
4. Shake or tap the sensor to enter Bluetooth mode
5. Select device number from the scan results

Controls
Ctrl+P = Open command menu
Ctrl+C = End program

Menu (Ctrl+P) Options:
1. Send command to sensor
2. Enable/disable HTTP forwarding
3. Toggle CR+LF
4. Generate diagnostic report NOW
5. Toggle auto-report (ON/OFF)
6. Back to receive mode
7. Quit

Sensor Commands
- SYS_RESET   = Reset sensor (sensor restart it will disconnect BLE)
- SYS_OPEN    = Open receiving mode (sensor restart it will disconnect BLE)
- SYS_SLEEP   = Sleep mode (sensor will disconnect BLE)
- SYS_INFO    = Get sensor info
- S1_DEPTH    = Set actual depth main sensor (in cm)
- S2_DEPTH    = Set actual depth secondary sensor (in cm) #in TRX Case this will be not used
- NB_SHOW     = Show system info enable/disable
- TEST_PACKET = Test packet 06 (triggers automatic diagnostic report)
- DISTANCE    = Built-in distance sensor readings

📊 Diagnostic Reports
After sending TEST_PACKET, the system will automatically:
1. Monitor the complete NB-IoT transmission sequence
2. Analyze all AT commands and responses
3. Evaluate each layer: SIM → Registration → PDP → UDP
4. Generate a professional PDF report in the 'reports/' folder

Reports include:
- ✅/❌ Status for each network layer
- 📊 Signal quality metrics (RSRP, SNR)
- 🔴 Root cause analysis if failed
- 🔧 Specific recommended actions
- 📦 Packet transmission details

Report Files
Location: reports/
Format: Network_Report_[IMEI]_[TIMESTAMP]_#[NUMBER].pdf
Example: Network_Report_093982_20260212_143015_#001.pdf

Package Contents
- Start.bat              = Auto-launcher script
- Scanner.py             = Main application with diagnostics
- NetworkDiagnostics.py  = Log analysis engine
- PDFReportGenerator.py  = PDF report creator
- README.txt             = This file

Version History
V0.2.0 (2026-02-12)
- Added automatic network diagnostics
- Added PDF report generation
- Added signal quality evaluation
- Added root cause analysis
- Added report history tracking

V0.1.2 (2026-01-26)
- Initial release with BLE and HTTP support
