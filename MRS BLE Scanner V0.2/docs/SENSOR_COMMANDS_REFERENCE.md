# MRS NB-IoT Sensor - Working Commands Reference

**Device**: MRS M06 NB-IoT Dustbin Sensor  
**Firmware**: V1.0.01  
**Manufacturer**: NHR  

---

## ✅ CONFIRMED WORKING COMMANDS

All commands below have been tested and verified to work on the actual hardware.

---

## 📋 Custom Sensor Commands

### Help & Information

#### `?`
**Purpose**: Show complete command list  
**Response**: Full menu of 60 available commands  
**Usage**: Send `?` to see all commands

```
0. ?
1. CMD_1 through CMD_9
10. CMD_LIST
11. SYS_RESET
12. SYS_INFO
13. SENSOR_SHOW
14. READ_SET
15. TIMESTAMP?
16. UART_SHOW
17. UART_SEND=
18. FORCE_ALIVE
19. FIFO_SHOW
20. FORCE_ATTACH
21. COTA_CFG
22. DATE:
23. TIME:
24. NOW
25. SET_IP
26. SET_PORT
27. SET_ALIVE
28. SET_SENSOR
29. S1_DEPTH
30. S2_DEPTH
31. SET_S_MON
32. SET_S_RCNT
33. PD_START
34. PD_6AXIS
35. PD_TX
36. PD_SLEEP
37. SYS_OPEN
38. SYS_SLEEP
39. DISTANCE
40. 6AXIS_RESET
41. SENSOR_RESET
42. LORA_SHOW
43. NB_SHOW
44. VOLTAGE
45. DIS_KEEP
46. VOL_RECORD
47. VOL_CLEAR
48. SEND_VREC
49. TEST_PACKET
50. RP_FG
51. REPORT
52. S1_DIS_LV
53. S2_DIS_LV
54. DETECT_MODE
55. KEEP_DETECT
56. BL_NAME
57. COVER_CHK
58. COVER_ALARM
59. SELECT_DETECT
```

---

### Essential Commands

#### `NB_SHOW`
**Purpose**: Enable UART logging mode  
**Response**: `CMD_UART_LOG_MODE ENABLE.`  
**Usage**: **ALWAYS send this first** to see AT commands and diagnostics  
**Example**:
```
> NB_SHOW
< CMD_UART_LOG_MODE ENABLE.
```

#### `TEST_PACKET`
**Purpose**: Run full network diagnostic test  
**Response**: `try to send 06 packet`  
**Duration**: 30-60 seconds  
**Auto-generates PDF report**: Yes  
**What it does**:
- Reads IMEI and IMSI
- Configures NB-IoT bands (8, 28)
- Sets APN (nxt20.net)
- Attempts network registration
- Tries to get IP address
- Sends test data to server
- Shuts down modem
- Generates diagnostic report

**Example**:
```
> TEST_PACKET
< try to send 06 packet
[... network sequence runs ...]
< AT+CFUN=0
[Report auto-generated: R2464-14.30.pdf]
```

---

### Sensor Reading Commands

#### `DISTANCE`
**Purpose**: Get distance sensor readings  
**Response**: `distance: 2 cm ,2 cm`  
**Returns**: s1 and s2 sensor distances in cm

#### `ANGLE`
**Purpose**: Get accelerometer angle  
**Response**: Returns distance reading (sensor data)

#### `IMU`
**Purpose**: Get IMU (accelerometer) data  
**Response**: `angle : x=88 ,y=-1 ,z=0`  
**Returns**: 3-axis angle data

---

### Configuration Commands

#### `SET_IP`
**Purpose**: Set server IP address  
**Usage**: `SET_IP=xxx.xxx.xxx.xxx`

#### `SET_PORT`
**Purpose**: Set server port  
**Usage**: `SET_PORT=xxxx`

#### `SET_ALIVE`
**Purpose**: Set keep-alive interval

#### `S1_DEPTH`
**Purpose**: Set sensor 1 depth calibration

#### `S2_DEPTH`
**Purpose**: Set sensor 2 depth calibration

---

### System Commands

#### `SYS_RESET`
**Purpose**: Reset the system

#### `SYS_INFO`
**Purpose**: Get system information

#### `VOLTAGE`
**Purpose**: Get battery voltage

#### `SENSOR_SHOW`
**Purpose**: Show sensor status

#### `REPORT`
**Purpose**: Generate report manually

---

## 📡 AT Commands (NB-IoT Modem)

### Device Information

```
ATI                    # Device info (Manufacturer, Model, Revision, IMEI)
ATI2                   # Additional info
ATI8                   # Additional info
AT+CGSN=1              # Get IMEI
AT+CIMI                # Get IMSI (SIM card number)
AT+CGMR                # Get firmware revision
```

**Example ATI Response**:
```
Manufacturer: NHR
Model: M06
Revision: V1.0.01
IMEI: 351469520162464
```

---

### Network Registration

```
AT+CEREG?              # Check registration status
AT+CEREG=0             # Disable registration updates
AT+CEREG=2             # Enable detailed registration updates
AT+CFUN=0              # Disable modem (minimum functionality)
AT+CFUN=1              # Enable modem (full functionality)
AT+CFUN=4              # Airplane mode
```

**Registration Status Codes**:
- `+CEREG: 0` = Not registered, not searching
- `+CEREG: 1` = Registered, home network ✅
- `+CEREG: 2` = Not registered, searching 🔄
- `+CEREG: 2,2` = Not registered, searching (detailed) 🔄
- `+CEREG: 3` = Registration denied ❌
- `+CEREG: 5` = Registered, roaming ✅

---

### Network Configuration

```
AT+QCBAND=0,8,28                    # Set NB-IoT bands (8, 28)
AT+CGDCONT=1,"IP","nxt20.net"       # Set APN
AT+CGPADDR=0                        # Check IP for context 0
AT+CGPADDR=1                        # Check IP for context 1
AT+CGACT?                           # Check PDP context activation
```

---

### Connection & Socket

```
AT+CIPOPEN?            # Check TCP/UDP connection status
AT+QICFG?              # Query socket configuration
AT+CIPTIMEOUT=20000,20000,10000    # Set connection timeouts
```

---

### Power Management

```
AT+CPSMS=0             # Disable power saving mode
AT+CPSMS?              # Query power saving mode
AT+QCSLEEP=0           # Disable sleep mode
AT+QPSMEXTCFG?         # Query extended PSM config
```

---

### Configuration & Settings

```
ATE0                   # Disable command echo
AT+QCLEDMODE=0         # Configure LED mode
AT+QCPMUCFG=0          # PMU configuration
AT&V                   # View current configuration
AT+QURCCFG?            # Query URC configuration
AT+QCFG="urc/delay"    # Query URC delay config
```

---

### Advanced/Vendor Specific

```
AT+QNBIOTEVENT?        # Query NB-IoT events
AT+QSUBSYSVER          # Get subsystem versions
AT+QNITZ?              # Query network time
AT+QFOTADL?            # Query FOTA download status
AT+QFLST               # List files in flash
```

---

## 📊 Sensor Data Formats

### Distance Readings
```
s1:2 cm(3%) ,s2:2 cm(3%) => [lv1] , cnt:0/10 min
```
- **s1**: Sensor 1 distance (cm and percentage full)
- **s2**: Sensor 2 distance (cm and percentage full)
- **lv1/lv2/lv3**: Fill level (1=low, 2=medium, 3=high)
- **cnt**: Event counter (events/10 minutes)

### Lid Status
```
<<< [Close] chang to [Open] >>>    # Lid opened
<<< [Open] chang to [Close] >>>    # Lid closed
Open -> Open                        # Lid still open
Close -> Close                      # Lid still closed
```

### Accelerometer (IMU)
```
angle : x=89 ,y=0 ,z=0
read (x=89, y=0, z=0) , BG (x=90, y=0, z=0)
6 axis interrupt ...
```

### Distance Sensor (Raw)
```
distance: s1 20 mm ,s2 20 mm
distance: 2 cm ,2 cm
```

---

## 🔧 Quick Start Guide

### 1. First Connection
```
1. Connect to sensor via BLE
2. Send: NB_SHOW
3. Wait for: CMD_UART_LOG_MODE ENABLE.
```

### 2. Run Full Diagnostic
```
1. Send: NB_SHOW
2. Send: TEST_PACKET
3. Wait 30-60 seconds
4. Report auto-generates: R2464-14.30.pdf
```

### 3. Check Network Status
```
1. Send: NB_SHOW
2. Send: AT+CEREG?
3. Check response: +CEREG: 2,1 (registered) or +CEREG: 2,2 (searching)
4. Send: AT+CGPADDR=1
5. Check if IP assigned
```

### 4. Manual Report Generation
```
1. Press Ctrl+P in scanner
2. Choose option 4
3. Report generates immediately
```

---

## 📝 Report Naming

**Format**: `R{last4digits}-{HH.MM}.pdf`

**Examples**:
- `R2464-14.30.pdf` = Device ending in 2464, generated at 2:30 PM
- `R0687-09.15.pdf` = Device ending in 0687, generated at 9:15 AM

**Last 4 digits** = Last 4 digits of IMEI  
**HH.MM** = Time in 24-hour format

---

## ⚠️ Important Notes

1. **Always send `NB_SHOW` first** - Without this, you won't see any AT commands or diagnostics
2. **`TEST_PACKET` auto-generates reports** - No need to manually generate after TEST_PACKET
3. **Network registration takes time** - Device will retry multiple times before giving up
4. **Reports overwrite if same device + same minute** - This is intentional, keeps only latest
5. **AT commands are case-sensitive** - Use exact capitalization shown

---

## 🎯 Command Categories Summary

| Category | Commands | Purpose |
|----------|----------|---------|
| **Essential** | `NB_SHOW`, `TEST_PACKET`, `?` | Must-know commands |
| **Sensor** | `DISTANCE`, `ANGLE`, `IMU` | Read sensor data |
| **Config** | `SET_IP`, `SET_PORT`, `S1_DEPTH`, `S2_DEPTH` | Configure device |
| **System** | `SYS_RESET`, `SYS_INFO`, `VOLTAGE` | System management |
| **Network** | `AT+CEREG?`, `AT+CGPADDR`, `AT+CFUN` | Network status |
| **Power** | `AT+CPSMS`, `AT+QCSLEEP`, `AT+CFUN=0` | Power management |

---

**Last Updated**: 2026-02-14  
**Source**: Firmware analysis + live testing on device 351469520162464
