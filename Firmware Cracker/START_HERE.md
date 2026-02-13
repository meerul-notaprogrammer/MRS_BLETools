# 🔓 FIRMWARE CRACKER - COMPLETE PACKAGE

## ✅ What You Now Have

A complete toolkit to extract ALL intelligence from your NB-IoT sensor firmware via BLE connection.

---

## 📁 Package Contents

```
Firmware Cracker/
├── 🚀 Start_Firmware_Cracker.bat    ← DOUBLE-CLICK TO RUN
├── 🐍 CrackFirmware.py              ← Main launcher script
├── 🧠 FirmwareIntelligence.py       ← Intelligence extraction engine
├── 📖 README.md                      ← Full documentation
├── 🎯 INTELLIGENCE_TARGETS.md       ← What gets extracted
└── 📊 reports/                       ← Generated intelligence reports
```

---

## 🎯 Mission Objectives

### PRIMARY OBJECTIVE: Find Server Configuration
```
✓ Remote Server IP Address
✓ Remote Server Port
✓ Protocol Type (UDP/TCP)
✓ Connection ID
```

### SECONDARY OBJECTIVES: Device Intelligence
```
✓ IMEI (Device Identity)
✓ IMSI (SIM Identity)
✓ ICCID (SIM Card ID)
✓ Firmware Version
✓ Manufacturer & Model
✓ Local IP Address
✓ APN Configuration
✓ Signal Quality (RSRP/SNR)
✓ Network Registration Status
✓ Power Management Settings
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Tool
```
Double-click: Start_Firmware_Cracker.bat
```

### Step 2: Select Your Sensor
```
Found 5 devices:
  1. N_01E1_N6BR1_687041    XX:XX:XX:XX:XX:XX
  2. iPhone                  YY:YY:YY:YY:YY:YY
  
Select device number: 1
```

### Step 3: Wait for Extraction
```
[IDENTITY] Probing 8 commands...
[NETWORK] Probing 8 commands...
[SOCKET_CONFIG] Probing 6 commands...  ← CRITICAL!
...
[COMPLETE] Intelligence extraction complete!
```

---

## 📊 What You'll Get

### Screen Output
```
INTELLIGENCE SUMMARY
================================================================================
[DEVICE IDENTITY]
  IMEI                : 351469520687041
  IMSI                : 502153012345678
  FIRMWARE_VERSION    : BG96MAR02A07M1G

[NETWORK ENDPOINTS]
  Local IP            : 10.123.45.67
  Remote Servers      :
    → 103.xxx.xxx.xxx  ← WHERE YOUR DATA GOES!

  UDP Connections:
    +CIPOPEN: 0,"UDP","103.xxx.xxx.xxx",5000
                        ^^^^^^^^^^^^^^^^  ^^^^
                        SERVER IP         PORT
```

### JSON Report
```
reports/firmware_intelligence_20260213_124500.json
```

Contains complete structured data for programmatic access.

---

## 🎯 Next Steps After Extraction

### Option 1: Redirect Server via AT Commands
```python
# You now know: Remote IP = 103.xxx.xxx.xxx, Port = 5000

# Send these commands via BLE:
AT+CIPCLOSE=0                           # Close current connection
AT+CIPOPEN=0,"UDP","YOUR_IP",YOUR_PORT  # Open to YOUR server
AT+CIPOPEN?                             # Verify redirection
```

### Option 2: Build Your Own Server
```python
# You know the protocol and data format
# Build a UDP server listening on port 5000
# Parse incoming sensor data packets
```

### Option 3: Develop Custom Firmware
```python
# You know:
# - AT command set supported
# - Device capabilities
# - Network configuration
# - Data transmission format

# Build custom firmware that:
# - Reads sensors
# - Sends to YOUR server
# - Uses YOUR protocol
```

---

## 🔍 How It Works

### 1. BLE Connection
```
Scanner → BLE → Sensor
         (Nordic UART Service)
```

### 2. AT Command Probing
```
For each command in list:
  Send: AT+COMMAND
  Wait: 3 seconds
  Capture: All responses
  Parse: Extract intelligence
```

### 3. Intelligence Extraction
```
Raw Responses → Parser → Structured Data
                         ↓
                    JSON Report
```

### 4. Analysis
```
Structured Data → Network Endpoint Extractor
                → Device Identity Extractor
                → Configuration Analyzer
                         ↓
                  Intelligence Summary
```

---

## 📋 AT Commands Probed (42 Total)

### Critical Commands (Server Discovery)
```
✓ AT+CIPOPEN?     - Active connections
✓ AT+CIPSTATUS    - Connection status
✓ AT+CIPSHOW?     - Remote IP/port
✓ AT+NETSTAT      - Network statistics
✓ AT+CGPADDR      - Local IP
```

### Identity Commands
```
✓ AT+CGSN   - IMEI
✓ AT+CIMI   - IMSI
✓ AT+CCID   - ICCID
✓ AT+CGMR   - Firmware version
✓ AT+CGMI   - Manufacturer
✓ AT+CGMM   - Model
```

### Network Commands
```
✓ AT+CEREG?      - Registration status
✓ AT+COPS?       - Operator
✓ AT+CSQ         - Signal quality
✓ AT+QCBCINFOSC  - Cell info (RSRP/SNR)
✓ AT+CGDCONT?    - APN configuration
```

### Configuration Commands
```
✓ AT+QCSLEEP?    - Sleep mode
✓ AT+CPSMS?      - Power saving
✓ AT&V           - Full config dump
```

---

## ⚠️ Important Notes

### ✅ What This Tool DOES
- ✓ Reads firmware configuration
- ✓ Extracts network settings
- ✓ Discovers server endpoints
- ✓ Maps AT command capabilities
- ✓ Generates intelligence reports

### ❌ What This Tool DOES NOT Do
- ✗ Modify firmware
- ✗ Change device settings
- ✗ Extract firmware binary
- ✗ Require hardware tools
- ✗ Need physical access to PCB

### 🔒 Legal & Ethical Use
- ✓ Only use on devices you own
- ✓ Only use with permission
- ✓ Respect privacy and security
- ✓ Follow local regulations

---

## 🛠️ Troubleshooting

### No devices found?
```
✓ Check Bluetooth is enabled
✓ Sensor must be powered on
✓ Move closer (within 10-30m)
```

### No AT command responses?
```
✓ Sensor might be in deep sleep
✓ Try during active transmission window
✓ Send "AT" first to wake device
```

### Partial data only?
```
✓ Some commands need active network
✓ Try when sensor is transmitting
✓ Increase timeout in code
```

---

## 📞 Support & Documentation

- **README.md** - Full usage guide
- **INTELLIGENCE_TARGETS.md** - What gets extracted
- **FirmwareIntelligence.py** - Source code with comments

---

## 🎓 Learning Resources

### Understanding AT Commands
- AT commands are text-based commands for modems
- Format: `AT+COMMAND?` (query), `AT+COMMAND=value` (set)
- Responses are text strings

### Understanding NB-IoT
- NB-IoT = Narrowband Internet of Things
- Low-power, wide-area cellular technology
- Uses UDP/TCP over cellular network

### Understanding BLE
- BLE = Bluetooth Low Energy
- Nordic UART Service = Serial communication over BLE
- Used for local debugging/configuration

---

## 🚀 Ready to Crack?

```
cd "Firmware Cracker"
Start_Firmware_Cracker.bat
```

**Let's extract that intelligence! 🔓**

---

**Made with 🔍 for sensor reverse engineering**
