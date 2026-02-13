---
name: Sensor Diagnostics
description: Complete knowledge model for MRS-BLE-Scanner NB-IoT sensor stack - architecture, AT commands, network diagnostics, and troubleshooting
---

# 🧠 SENSOR KNOWLEDGE PACKAGE

## 1️⃣ Device Architecture Overview

### Hardware Stack

| Layer | Component | Purpose |
|-------|-----------|---------|
| MCU | Main controller | Sensor logic, command handling |
| BLE | Nordic UART Service | Local debugging & configuration |
| NB-IoT Modem | NHR M06 | Cellular uplink |
| SIM | Maxis NB-IoT | Network authentication |
| Sensors | Ultrasonic (s1, s2) | Distance measurement |
| IMU | 6-axis | Angle detection |
| Power | Battery | Long-life deployment |

### Key Principle
- **BLE = Local debugging + configuration only**
- **Production data = NB-IoT**

---

## 2️⃣ Communication Layers

### BLE Layer (Local Debug)

**Service UUID:**
```
6e400001-b5a3-f393-e0a9-e50e24dcca9e
```

**Characteristics:**

| UUID | Mode | Purpose |
|------|------|---------|
| `6e400002` | Write | Send commands |
| `6e400003` | Notify | Receive logs |

### NB-IoT Stack

**Connection Flow:**
```
SIM Ready
    ↓
CEREG Registration
    ↓
NETOPEN
    ↓
CIPOPEN (UDP)
    ↓
CIPSEND
    ↓
CIPRXGET (ACK)
    ↓
CIPCLOSE
    ↓
NETCLOSE
    ↓
Sleep
```

---

## 3️⃣ AT Command Meaning Map

### Registration Commands

| Command | Meaning |
|---------|---------|
| `AT+CEREG?` | Check network registration |
| `+CEREG: 0,1` | Registered (Home) |
| `+CEREG: 0,5` | Registered (Roaming) |
| `+CEREG: 2,2` | Searching (Not attached) |
| `+CEREG: 0,3` | Registration denied |

### Signal Quality

**From:** `+QCBCINFOSC: earfcn,pci,RSRP,SNR,...`

| Field | Meaning |
|-------|---------|
| RSRP | Signal power (dBm) |
| SNR | Signal-to-noise ratio (dB) |

#### Quick Signal Formula

**RSRP Quality:**

| RSRP (dBm) | Quality |
|------------|---------|
| -70 to -85 | Excellent |
| -85 to -95 | Good |
| -95 to -105 | Weak |
| < -110 | Poor |

**SNR Quality:**

| SNR (dB) | Quality |
|----------|---------|
| > 5 | Excellent |
| 0 to 5 | Good |
| -5 to 0 | Marginal |
| < -10 | Poor |

---

## 4️⃣ Packet Transmission Structure

### Example Packet
```
0654351469520520687041006698D6C76590000000000000007
```

### General Structure
```
[Header]
[IMEI]
[Sensor Payload]
[Checksum]
```

### Length Confirmation
```
+CIPSEND: 1,51,51
```
**Meaning:** 51 bytes sent, 51 acknowledged

---

## 5️⃣ Common Failure Points

### Layer-by-Layer Debug Tree

```
Layer 1: SIM
    ├─ SIM Ready?
    ├─ IMSI visible?
    └─ IMEI allowed?

Layer 2: Registration
    ├─ CEREG=1 or 5? → Continue
    ├─ CEREG=2 → Searching
    └─ CEREG=3 → Rejected

Layer 3: PDP
    ├─ NETOPEN success?
    └─ APN correct? ("m2mxnbiot")

Layer 4: UDP
    ├─ CIPOPEN success?
    ├─ CIPSEND confirmed?
    └─ ACK received?
```

---

## 6️⃣ Power Behavior Model

### After Send
```
AT+QCSLEEP=0
+QCSLEEP: HIB2
```

**Meaning:**
- Modem enters hibernate
- Battery preserved

### Warning: Repeated Searching
```
CEREG=2 loop
```
**Result:** Battery drains rapidly

---

## 7️⃣ Sensor Internal Logic

### REPORT Command
```
REPORT=6,1
```

**Meaning:**
- All report intervals = 1 minute

**Default Triggers:**
- open
- timeout
- <20%
- periodic

### Motion Trigger
```
6 axis interrupt ...
```

**Meaning:**
- IMU detected movement
- Wakes system

---

## 8️⃣ Network Modes

**From:** `+QCSTATUS: PHY`

| Mode | Meaning |
|------|---------|
| `NBMode: "Stand alone"` | Dedicated NB-IoT carrier |
| `NBMode: "Guard Band"` | Shared LTE band |

**Both modes are valid.**

---

## 9️⃣ Complete Diagnostic Formula (Quick Method)

### Evaluation Order

```
SIM Ready?
    ↓
IMSI visible?
    ↓
CEREG?
    ├─ 1 or 5 → continue
    ├─ 2 → searching
    └─ 3 → rejected
    ↓
NETOPEN success?
    ↓
CIPOPEN success?
    ↓
CIPSEND confirmed?
    ↓
ACK received?
    ↓
RSRP & SNR acceptable?
```

**If all pass → Device healthy.**

---

## 🔧 Diagnostic Workflow

When analyzing sensor logs, follow this systematic approach:

### Step 1: Initial Health Check
1. Check SIM status
2. Verify IMSI/IMEI
3. Confirm CEREG registration

### Step 2: Network Quality
1. Extract RSRP value
2. Extract SNR value
3. Apply quality formulas

### Step 3: Connection Verification
1. Verify NETOPEN
2. Verify CIPOPEN
3. Check CIPSEND acknowledgment

### Step 4: Data Transmission
1. Verify packet structure
2. Confirm byte count match
3. Check for ACK

### Step 5: Power Analysis
1. Check sleep mode entry
2. Identify any search loops
3. Assess battery impact

---

## 📊 Common Log Patterns

### Healthy Device
```
SIM Ready
AT+CIMI → [IMSI]
AT+CEREG? → +CEREG: 0,1
AT+QCBCINFOSC → RSRP: -85, SNR: 8
AT+NETOPEN → OK
AT+CIPOPEN → OK
AT+CIPSEND → +CIPSEND: 1,51,51
AT+QCSLEEP=0 → +QCSLEEP: HIB2
```

### Searching Device
```
AT+CEREG? → +CEREG: 2,2
[Repeated CEREG checks]
[No NETOPEN]
[Battery drain]
```

### Rejected Device
```
AT+CEREG? → +CEREG: 0,3
[Registration denied]
[Check SIM/IMEI whitelist]
```

---

## 🎯 Usage Instructions

When the user provides sensor logs:

1. **Identify the connection phase** (SIM → Registration → PDP → UDP)
2. **Extract signal metrics** (RSRP, SNR)
3. **Apply quality formulas**
4. **Follow the diagnostic tree**
5. **Provide specific diagnosis** with layer identification
6. **Suggest targeted fixes** based on failure point

### Example Analysis Format

```
📍 Layer: [SIM/Registration/PDP/UDP]
🔍 Issue: [Specific problem]
📊 Metrics: RSRP: [value] ([quality]), SNR: [value] ([quality])
💡 Diagnosis: [Root cause]
🔧 Fix: [Specific action]
```

---

## 🚨 Critical Reminders

1. **CEREG is king** - Always check registration first
2. **Signal quality matters** - Poor RSRP/SNR = connection issues
3. **ACK confirms success** - No ACK = packet lost
4. **Search loops kill battery** - CEREG=2 repeatedly = problem
5. **APN must be exact** - "m2mxnbiot" for Maxis NB-IoT

---

## 📚 Reference Tables

### CEREG Status Codes
| Code | Status | Action |
|------|--------|--------|
| 0,0 | Not registered, not searching | Check SIM |
| 0,1 | Registered, home network | ✅ Good |
| 0,2 | Not registered, searching | Wait or check signal |
| 0,3 | Registration denied | Check IMEI whitelist |
| 0,5 | Registered, roaming | ✅ Good |

### Sleep Modes
| Mode | Meaning | Power |
|------|---------|-------|
| HIB2 | Hibernate level 2 | Ultra-low |
| ACTIVE | Modem active | High |

---

## 🔄 Version History
- v1.0 - Initial knowledge package creation
