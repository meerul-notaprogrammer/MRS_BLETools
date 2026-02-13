# 🔄 **REVISED STRATEGY - Custom Protocol Reverse Engineering**

## 🎯 **Major Discovery**

The sensor **does NOT use standard AT commands**! Instead:

- ❌ **NOT** a Quectel modem with AT commands
- ✅ **IS** a custom MCU with proprietary protocol
- ✅ **HAS** custom command interface
- ✅ **STREAMS** real-time sensor data

---

## 📊 **What We Discovered**

### Working Custom Commands

| Command | Response | Data Type |
|---------|----------|-----------|
| `ATI` | `<<< [Open] chang to [Close] >>>` | State change |
| `ATI` | `read (x=89, y=0, z=0) , BG (x=90, y=0, z=0)` | IMU calibration |
| `ATI2` | `s1:2 cm(3%) ,s2:5 cm(9%) => [lv1] , cnt:0/10 min` | **Sensor data** |
| `ATI8` | `angle : x=89 ,y=0 ,z=0` | **IMU angles** |
| `AT+QFOTADL?` | `distance: s1 20 mm ,s2 20 mm` | **Distance** |

### Data Formats Discovered

#### Sensor Reading Format
```
s1:2 cm(3%) ,s2:5 cm(9%) => [lv1] , cnt:0/10 min
│   │    │      │    │        │         └─ Report counter (0-10)
│   │    │      │    │        └─ Fill level (lv1, lv2, lv3...)
│   │    │      │    └─ Sensor 2 percentage
│   │    │      └─ Sensor 2 distance in cm
│   │    └─ Sensor 1 percentage
│   └─ Sensor 1 distance in cm
└─ Sensor identifier
```

#### IMU Format
```
angle : x=89 ,y=0 ,z=0
        └─ X, Y, Z axis angles in degrees
```

#### Distance Format
```
distance: s1 20 mm ,s2 20 mm
          └─ Sensor 1 & 2 in millimeters
```

---

## 🔧 **NEW TOOLS CREATED**

### 1. Custom Protocol Analyzer (`CustomProtocolAnalyzer.py`)
- Brute forces **200+ command variations**
- Tests all possible command patterns:
  - ATI variants (ATI0-ATI99)
  - Configuration commands (CONFIG, SET, GET, etc.)
  - Server commands (SERVER, HOST, IP, PORT, etc.)
  - Network commands (NETWORK, APN, CONNECT, etc.)
  - Firmware commands (VERSION, UPDATE, BOOTLOADER, etc.)
  - Debug commands (DEBUG, LOG, TRACE, etc.)
  - Help commands (HELP, ?, COMMANDS, etc.)
- Categorizes responses by data type
- Maps complete protocol

### 2. Protocol Cracker Launcher (`ProtocolCracker.py`)
- Easy-to-use interface
- Automatic device scanning
- Complete command discovery
- JSON report generation

### 3. Batch Launcher (`Start_Protocol_Cracker.bat`)
- One-click execution
- Windows-friendly

---

## 🚀 **HOW TO USE**

### Step 1: Run Protocol Cracker
```bash
cd "c:\document\MRS-BLE-Scanner-V0.1.2\Firmware Cracker"
Start_Protocol_Cracker.bat
```

### Step 2: Wait for Analysis
- Tests 200+ commands
- Takes 5-10 minutes
- Keep sensor in BLE range

### Step 3: Review Results
```bash
# Open the generated report
reports/protocol_map_YYYYMMDD_HHMMSS.json
```

### Step 4: Find Configuration Commands
Look for commands that might:
- Set server IP/port
- Configure network
- Update firmware
- Access bootloader

---

## 🎯 **WHAT WE'RE LOOKING FOR**

### Critical Commands to Find

1. **Server Configuration**
   ```
   SETSERVER <ip> <port>
   SETHOST <hostname>
   SETURL <url>
   CONFIG_SERVER=<ip>:<port>
   ```

2. **Network Configuration**
   ```
   SETAPN <apn>
   SETNETWORK <config>
   CONNECT <server>
   ```

3. **Firmware Access**
   ```
   BOOTLOADER
   DFU
   UPDATE
   FLASH
   DUMP
   ```

4. **Configuration Interface**
   ```
   CONFIG?
   SHOWCONFIG
   LISTCONFIG
   GETCONFIG
   ```

---

## 📋 **NEXT STEPS**

### Immediate (After Protocol Cracker)
1. ✅ Run `Start_Protocol_Cracker.bat`
2. ✅ Review `protocol_map_*.json`
3. ✅ Identify configuration commands
4. ✅ Test server configuration

### Short Term
1. Find server config commands
2. Test changing server IP/port
3. Verify data redirection works
4. Document complete protocol

### Long Term
1. Extract firmware binary (if possible)
2. Disassemble and analyze
3. Build custom firmware
4. Add new features

---

## 💡 **WHY THIS IS BETTER**

### Advantages of Custom Protocol
- ✅ Direct access to sensor data
- ✅ Real-time streaming
- ✅ Custom command interface
- ✅ Potentially simpler configuration
- ✅ No modem abstraction layer

### What We Can Do
- ✅ Map complete command set
- ✅ Find configuration interface
- ✅ Understand data protocol
- ✅ Build custom tools
- ✅ Potentially easier to modify

---

## 🔍 **ARCHITECTURE UNDERSTANDING**

### Current Architecture
```
┌─────────────────────────────────────────┐
│         Custom MCU Firmware             │
│  (Nordic nRF52 or similar)              │
├─────────────────────────────────────────┤
│  Custom Command Interface               │
│  - ATI variants (sensor data)           │
│  - Unknown config commands              │
│  - State machine                        │
├─────────────────────────────────────────┤
│  Sensors                                │
│  - Ultrasonic (s1, s2)                  │
│  - IMU (6-axis)                         │
├─────────────────────────────────────────┤
│  Communication                          │
│  - BLE (Nordic UART) ← Debug/Config     │
│  - NB-IoT Modem ← Production Data       │
└─────────────────────────────────────────┘
```

### Data Flow
```
Sensors → MCU Firmware → BLE (debug/config)
                      ↓
                  NB-IoT Modem → Server
```

---

## 📚 **DOCUMENTATION**

### Read These Files
1. **NEW_APPROACH_CUSTOM_PROTOCOL.md** ← This file
2. **CustomProtocolAnalyzer.py** ← Source code
3. **ProtocolCracker.py** ← Launcher
4. **protocol_map_*.json** ← Results (after running)

### Original Files (Still Useful)
- **FIRMWARE_DEVELOPMENT_GUIDE.md** ← Firmware dev guide
- **MASTER_INDEX.md** ← Toolkit overview

---

## ⚠️ **IMPORTANT NOTES**

### What Changed
- ❌ AT command approach doesn't work
- ✅ Custom protocol approach is needed
- ✅ New tools created for this

### What Stayed the Same
- ✅ Goal: Extract all intelligence
- ✅ Goal: Redirect server
- ✅ Goal: Build custom firmware
- ✅ BLE communication method

---

## 🎉 **READY TO CRACK THE PROTOCOL!**

Run this command to start:
```bash
Start_Protocol_Cracker.bat
```

**This will discover ALL working commands and map the complete protocol!**

---

**Made with 🔍 for custom protocol reverse engineering**
