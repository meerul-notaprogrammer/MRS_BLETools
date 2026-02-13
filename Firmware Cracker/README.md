# 🔓 Firmware Cracker

**Extract ALL intelligence from your NB-IoT sensor firmware via BLE**

## 🎯 What It Does

This tool connects to your sensor via Bluetooth and systematically probes it to extract:

### 📡 Network Configuration
- **UDP/TCP Connections** - Active socket connections
- **Remote Server IPs** - Where the sensor is sending data
- **Remote Ports** - Which ports are being used
- **Local IP Address** - Device's cellular IP
- **PDP Contexts** - Network configuration details

### 🆔 Device Identity
- **IMEI** - International Mobile Equipment Identity
- **IMSI** - International Mobile Subscriber Identity  
- **ICCID** - SIM Card ID
- **Manufacturer** - Device manufacturer
- **Model** - Device model number
- **Firmware Version** - Current firmware version

### ⚙️ AT Command Capabilities
- **Network Status** - Registration, signal quality, cell info
- **Power Management** - Sleep modes, power saving settings
- **Configuration** - Band settings, scan modes, IoT operation mode
- **Hidden Commands** - Vendor-specific commands

## 🚀 Quick Start

### Option 1: Double-click launcher
```
Run: Start_Firmware_Cracker.bat
```

### Option 2: Command line
```bash
cd "Firmware Cracker"
python CrackFirmware.py
```

## 📋 Usage

1. **Run the tool**
2. **Select your sensor** from the list of discovered BLE devices
3. **Wait for extraction** - The tool will probe ~50+ AT commands
4. **Review results** - Intelligence summary printed to screen
5. **Check JSON report** - Detailed report saved to `reports/` folder

## 📊 Output

### Screen Output
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    FIRMWARE INTELLIGENCE SCANNER                              ║
║                   Extracting All Device Information                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

[IDENTITY] Probing 8 commands...
[TX] AT+CGMI                     ✓
     Quectel
[TX] AT+CGSN                     ✓
     351469520687041

[SOCKET_CONFIG] Probing 6 commands...
[TX] AT+CIPOPEN?                 ✓
     +CIPOPEN: 0,"UDP","103.xxx.xxx.xxx",5000

INTELLIGENCE SUMMARY
================================================================================
[DEVICE IDENTITY]
  IMEI                : 351469520687041
  IMSI                : 502153012345678
  FIRMWARE_VERSION    : BG96MAR02A07M1G

[NETWORK ENDPOINTS]
  Local IP            : 10.123.45.67
  Remote Servers      :
    → 103.xxx.xxx.xxx

  UDP Connections:
    +CIPOPEN: 0,"UDP","103.xxx.xxx.xxx",5000
```

### JSON Report
Saved to: `reports/firmware_intelligence_YYYYMMDD_HHMMSS.json`

Contains complete structured data including:
- All AT command responses
- Parsed network endpoints
- Device identity
- Timestamp

## 🔍 What Gets Probed

### Command Categories

| Category | Commands | Purpose |
|----------|----------|---------|
| **Identity** | 8 | IMEI, IMSI, manufacturer, model, firmware |
| **Network** | 8 | Registration, signal, operator, cell info |
| **PDP Config** | 5 | IP addresses, PDP contexts |
| **Socket Config** | 6 | **Active connections, remote IPs/ports** |
| **Signal** | 3 | RSRP, SNR, cell measurements |
| **Power** | 3 | Sleep modes, power saving |
| **Config** | 6 | Band, scan mode, IoT settings |
| **Vendor** | 3 | Vendor-specific info |

**Total: ~42 AT commands probed**

## 🎯 Key Intelligence Targets

### Critical Commands for Server Discovery

```
AT+CIPOPEN?     → Shows active UDP/TCP connections
AT+CIPSTATUS    → Connection status with remote endpoints
AT+CIPSHOW?     → Remote IP and port details
AT+NETSTAT      → Network statistics
AT+CGPADDR      → Local IP address
```

### Example Output
```
+CIPOPEN: 0,"UDP","103.25.123.45",5000
```
This tells you:
- **Protocol**: UDP
- **Remote IP**: 103.25.123.45
- **Remote Port**: 5000

## 🛠️ Advanced Usage

### Probe Specific Category
```python
from FirmwareIntelligence import FirmwareIntelligence

# Only probe socket configuration
results = await scanner.probe_at_commands(category='socket_config')
```

### Custom AT Commands
Edit `FirmwareIntelligence.py` and add to `AT_COMMANDS` dict:
```python
'custom': [
    'AT+YOURCMD',
    'AT+ANOTHERCMD',
]
```

## 📁 File Structure

```
Firmware Cracker/
├── CrackFirmware.py          # Main launcher
├── FirmwareIntelligence.py   # Intelligence extraction engine
├── Start_Firmware_Cracker.bat # Windows launcher
├── README.md                  # This file
└── reports/                   # Generated intelligence reports
    └── firmware_intelligence_*.json
```

## ⚠️ Important Notes

1. **BLE Range**: Device must be within ~10-30m
2. **Scan Time**: Full scan takes ~2-3 minutes
3. **Active Connection**: Some commands only work when sensor is active
4. **No Modification**: This tool only READS, it doesn't modify firmware
5. **Legal Use**: Only use on devices you own or have permission to access

## 🔐 What You Can Do With This Data

### Server Redirection
Once you know the remote IP and port:
```python
# Send AT commands to redirect
AT+CIPCLOSE=0
AT+CIPOPEN=0,"UDP","YOUR_SERVER_IP",YOUR_PORT
```

### Network Analysis
- Understand data transmission patterns
- Identify bandwidth usage
- Monitor connection stability

### Firmware Development
- Know exact AT command set supported
- Understand device capabilities
- Plan custom firmware features

## 🚨 Troubleshooting

**No devices found?**
- Check Bluetooth is enabled
- Sensor must be powered on
- Try moving closer to sensor

**No responses to AT commands?**
- Sensor might be in sleep mode
- Try sending: `AT` first to wake it
- Check BLE characteristics are correct

**Partial data only?**
- Some commands require active network connection
- Try during sensor transmission window
- Increase timeout in code if needed

## 📞 Support

For issues or questions, check the main MRS BLE Scanner documentation.

---

**Made with 🔓 for sensor enthusiasts**
