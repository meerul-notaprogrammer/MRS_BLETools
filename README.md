# 🔵 MRS BLE Scanner Tools

**Professional BLE-based diagnostic tools for NB-IoT waste bin sensors.**

Connect to MRS NB-IoT sensors via Bluetooth Low Energy (BLE) to monitor, configure, and diagnose sensor health with professional PDF reporting.

---

## 📦 Download Individual Versions

| Version | Description | Download |
|---------|-------------|----------|
| **Scanner V0.1** | Basic BLE scanner — connect, send AT commands, monitor data | [⬇ Download V0.1](https://github.com/meerul-notaprogrammer/MRS_BLETools/releases/tag/v0.1) |
| **Scanner V0.2** | Advanced scanner — auto diagnostics, PDF reports, smart SIM detection | [⬇ Download V0.2](https://github.com/meerul-notaprogrammer/MRS_BLETools/releases/tag/v0.2) |
| **QuickServer** | Local test server — UDP receiver + web dashboard for sensor data | [⬇ Download QuickServer](https://github.com/meerul-notaprogrammer/MRS_BLETools/releases/tag/quickserver-v1.0) |
| **Firmware Cracker** | Firmware analysis tools — protocol cracking & deep extraction | [⬇ Download Firmware Cracker](https://github.com/meerul-notaprogrammer/MRS_BLETools/releases/tag/firmware-cracker-v1.0) |

> 💡 **Tip:** Click the download link → scroll down to **Assets** → download the **Source code (zip)**.

---

## 🔍 Version Comparison

| Feature | V0.1 | V0.2 |
|---------|:----:|:----:|
| BLE Connectivity | ✅ | ✅ |
| AT Command Support | ✅ | ✅ |
| Real-time Monitoring | ✅ | ✅ |
| HTTP Forwarding | ✅ | ✅ |
| Automatic Diagnostics | ❌ | ✅ |
| PDF Report Generation | ❌ | ✅ |
| Network Layer Analysis | ❌ | ✅ |
| Smart SIM Detection | ❌ | ✅ |
| Sensor Auto-Detection | ❌ | ✅ |
| Server Config Extraction | ❌ | ✅ |
| Root Cause Analysis | ❌ | ✅ |

---

## 🚀 Quick Start

### Scanner V0.1 (Basic)
```
1. Download V0.1
2. Run Start.bat
3. Select your sensor
4. Send commands via Ctrl+P menu
```

### Scanner V0.2 (Recommended)
```
1. Download V0.2
2. Run Start.bat
3. Select dustbin sensor (marked with green *)
4. Ctrl+P → Send NB_SHOW to see config
5. Ctrl+P → Send TEST_PACKET for diagnostics
6. Check reports/ folder for PDF report
```

### QuickServer (Local Testing)
```
1. Download QuickServer
2. Run Start.bat
3. Open http://localhost:5000 for dashboard
4. Configure sensor to send data to your local IP:8081
```

---

## 📋 Requirements

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **Hardware:** Bluetooth adapter (BLE compatible)
- **Dependencies:** Auto-installed on first run (`bleak`, `requests`, `colorama`)

---

## 📁 Repository Structure

```
MRS_BLETools/
├── MRS BLE Scanner V0.1/    # Basic BLE scanner
│   ├── Scanner.py           # Main application
│   ├── Start.bat            # Auto-launcher
│   └── README.txt           # Documentation
│
├── MRS BLE Scanner V0.2/    # Advanced diagnostic scanner
│   ├── Scanner.py           # Main application
│   ├── NetworkDiagnostics.py # Diagnostic engine
│   ├── PDFReportGenerator.py # PDF report generator
│   ├── Start.bat            # Auto-launcher
│   └── docs/                # Complete documentation
│
├── QuickServer/             # Local test server
│   ├── TestServer.py        # UDP + HTTP server
│   ├── dashboard.html       # Web dashboard
│   ├── Start.bat            # Auto-launcher
│   └── README.md            # Documentation
│
└── Firmware Cracker/        # Firmware analysis tools
    ├── CrackFirmware.py     # Basic firmware cracker
    ├── CrackFirmware_Deep.py # Deep extraction
    ├── ProtocolCracker.py   # Protocol analyzer
    └── Start_*.bat          # Launcher scripts
```

---

## 📝 License

Internal tool — MRS Development Team

---

*Last Updated: February 2026*
