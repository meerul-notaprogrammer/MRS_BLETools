# MRS BLE Scanner V0.2 - Upgrade Summary

## 🎯 What's New

### Automatic Network Diagnostics
- **Auto-detects** TEST_PACKET sequences
- **Monitors** complete NB-IoT transmission flow
- **Analyzes** AT commands using sensor diagnostics skill
- **Generates** PDF reports automatically

### Intelligent Analysis Engine
The system now understands the complete NB-IoT stack:

```
Layer 1: SIM
  ├─ SIM Ready?
  ├─ IMSI visible?
  └─ IMEI allowed?

Layer 2: Registration
  ├─ CEREG=1 or 5? → Continue
  ├─ CEREG=2 → Searching
  └─ CEREG=3 → Rejected

Layer 3: PDP Context
  ├─ NETOPEN success?
  └─ APN correct? ("m2mxnbiot")

Layer 4: UDP Socket
  ├─ CIPOPEN success?
  ├─ CIPSEND confirmed?
  └─ ACK received?
```

### Professional PDF Reports
Each report includes:
- ✅ Device information (IMEI, IMSI, timestamp)
- 📊 Layer-by-layer status (PASS/FAIL)
- 📡 Signal quality evaluation (RSRP, SNR)
- 🔴 Root cause analysis
- 🔧 Actionable recommendations
- 📦 Packet transmission details

## 📁 File Structure

```
MRS BLE Scanner V0.2/
├── Scanner.py              # Main application (upgraded)
├── NetworkDiagnostics.py   # Log analysis engine
├── PDFReportGenerator.py   # PDF report creator
├── Start.bat               # Launcher
├── README.txt              # Documentation
└── reports/                # Auto-generated reports
    ├── Network_Report_093982_20260212_143015_#001.pdf
    ├── Network_Report_093982_20260212_143245_#002.pdf
    └── ...
```

## 🔄 How It Works

### 1. Detection Phase
```python
# Scanner detects TEST_PACKET command
if 'TEST_PACKET' in data or 'try to send 06 packet' in data:
    self.test_packet_active = True
    # Start monitoring sequence
```

### 2. Monitoring Phase
```python
# Captures all AT commands and responses
self.diagnostics.add_log(timestamp, data)

# Detects sequence end markers:
# - AT+CIPCLOSE
# - AT+NETCLOSE
# - +QCSLEEP: HIB2
# - Multiple CEREG=2,2 (gave up)
```

### 3. Analysis Phase
```python
# Analyzes logs using diagnostic skill
result = self.diagnostics.analyze_logs(device_imei)

# Checks each layer:
# ✅ SIM Ready?
# ✅ IMSI visible?
# ✅ CEREG registered?
# ✅ NETOPEN success?
# ✅ CIPOPEN success?
# ✅ CIPSEND confirmed?
# ✅ ACK received?
```

### 4. Report Generation
```python
# Generates professional PDF
pdf_path = self.pdf_generator.generate_report(result, report_number)

# Saves to: reports/Network_Report_[IMEI]_[TIMESTAMP]_#[NUM].pdf
```

## 📊 Example Diagnostic Scenarios

### Scenario 1: HEALTHY Device
```
Input: TEST_PACKET
Logs show:
  ✅ SIM Ready
  ✅ +CEREG: 2,1 (Registered)
  ✅ +NETOPEN: 0
  ✅ +CIPOPEN: 1,0
  ✅ +CIPSEND: 1,51,51
  ✅ ACK received

Report:
  Status: HEALTHY
  All layers: PASS
  Recommendations: "All systems operating normally"
```

### Scenario 2: SEARCHING (Not Registered)
```
Input: TEST_PACKET
Logs show:
  ✅ SIM Ready
  ✅ IMSI: 502122020063253
  ❌ +CEREG: 2,2 (Searching)
  ❌ No NETOPEN
  ❌ No data sent

Report:
  Status: FAILED
  Failure Layer: Layer 2: Registration
  Root Cause: "Modem is searching for network but cannot register"
  Recommendations:
    - Move device to location with better NB-IoT coverage
    - Check if area has NB-IoT network coverage
    - Verify SIM is activated for NB-IoT service
    - Wait 2-3 minutes for network registration
```

### Scenario 3: PARTIAL (No ACK)
```
Input: TEST_PACKET
Logs show:
  ✅ SIM Ready
  ✅ +CEREG: 2,1 (Registered)
  ✅ +NETOPEN: 0
  ✅ +CIPOPEN: 1,0
  ✅ +CIPSEND: 1,51,51
  ❌ No ACK

Report:
  Status: PARTIAL
  Failure Layer: Layer 4: Server Response
  Root Cause: "Packet sent successfully but no ACK received from server"
  Recommendations:
    - Data was transmitted over NB-IoT network
    - Server may not have received the packet (UDP is connectionless)
    - Server may be offline or not responding
    - Check server logs to verify packet arrival
```

## 🎮 User Controls

### Menu Options (Ctrl+P)
```
1. Send command to sensor
2. HTTP forwarding mode [ACTIVE/OFF]
3. Toggle CR+LF (currently: ON/OFF)
4. Generate diagnostic report NOW  ← NEW!
5. Toggle auto-report (currently: ON/OFF)  ← NEW!
6. Back to receive mode
7. Quit
```

### Auto-Report Behavior
- **ON** (default): Automatically generates PDF after each TEST_PACKET
- **OFF**: Manual generation only (use option 4)

## 📈 Report History

Reports are automatically numbered and timestamped:
```
reports/
├── Network_Report_093982_20260212_140530_#001.pdf  (FAILED - Searching)
├── Network_Report_093982_20260212_141245_#002.pdf  (FAILED - Searching)
├── Network_Report_093982_20260212_142015_#003.pdf  (HEALTHY - Success!)
└── Network_Report_093982_20260212_143530_#004.pdf  (HEALTHY - Success!)
```

## 🔧 Technical Implementation

### NetworkDiagnostics.py
- Maintains rolling log buffer (last 500 entries)
- Pattern matching for AT commands
- Layer-by-layer status evaluation
- Signal quality formulas (RSRP/SNR)
- Root cause determination logic

### PDFReportGenerator.py
- ReportLab-based PDF generation
- Color-coded status indicators
- Professional table layouts
- Structured recommendations
- Packet hex display

### Scanner.py (Upgraded)
- Integrated diagnostics engine
- Async report generation
- Auto-detection of TEST_PACKET sequences
- Report counter and history
- Toggle controls for auto-report

## 🚀 Usage Example

```bash
# Start the scanner
> Start.bat

# Connect to device
Select device number: 4

# Enable NB_SHOW for detailed logs
Ctrl+P → 1 → NB_SHOW

# Send test packet
Ctrl+P → 1 → TEST_PACKET

# System automatically:
# 1. Detects TEST_PACKET
# 2. Monitors sequence
# 3. Analyzes logs
# 4. Generates PDF report

[DIAGNOSTIC] TEST_PACKET detected - monitoring sequence...
[DIAGNOSTIC] Sequence complete - analyzing logs...

========================================================================
[REPORT GENERATED] #001
========================================================================
  Status: FAILED
  Issue:  Layer 2: Registration
  File:   reports/Network_Report_093982_20260212_143015_#001.pdf
========================================================================
```

## 📋 Dependencies

```python
# Auto-installed by Scanner.py
- bleak          # BLE communication
- requests       # HTTP forwarding
- reportlab      # PDF generation
```

## 🎯 Benefits

### For End Users
- **No technical knowledge required** - Reports in plain English
- **Clear action items** - Specific steps to fix issues
- **Visual status** - Color-coded PASS/FAIL indicators
- **Historical tracking** - All reports saved with timestamps

### For Developers
- **Systematic diagnosis** - Layer-by-layer analysis
- **Pattern recognition** - Automatic AT command parsing
- **Extensible** - Easy to add new diagnostic rules
- **Reusable** - Diagnostic engine can be used standalone

## 🔮 Future Enhancements (V0.3?)

Potential additions:
- [ ] HTML report option
- [ ] Email report delivery
- [ ] Trend analysis across multiple reports
- [ ] Custom diagnostic rules
- [ ] Multi-device comparison
- [ ] Export to CSV/Excel
- [ ] Cloud storage integration

---

**Version:** 0.2.0  
**Date:** 2026-02-12  
**Author:** MRS Development Team  
**Powered by:** Sensor Diagnostics Skill + ReportLab
