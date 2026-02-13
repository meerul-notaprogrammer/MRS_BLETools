# MRS BLE Scanner V0.2 - Quick Test Script
# This script demonstrates how to test the diagnostic features

## Step-by-Step Testing Guide

### 1. Launch the Scanner
```bash
cd "c:\document\MRS-BLE-Scanner-V0.1.2\MRS BLE Scanner V0.2"
python Scanner.py
```

### 2. Initial Setup
- Press `Y` to agree to terms
- Press `ENTER` to skip HTTP (for testing)
- Wait for BLE scan to complete
- Select the dustbin sensor number (marked with green *)

### 3. Enable Detailed Logging (NB_SHOW)
**Purpose:** This enables AT command visibility in the logs

**Steps:**
1. Press `Ctrl+P` (opens menu)
2. Press `1` (send command)
3. Type: `NB_SHOW`
4. Press `ENTER`

**Expected Output:**
```
[TX] NB_SHOW
[RX] CMD_UART_LOG_MODE ENABLE
```

### 4. Send Test Packet (TEST_PACKET)
**Purpose:** Triggers the NB-IoT transmission sequence and auto-generates diagnostic report

**Steps:**
1. Press `Ctrl+P` (opens menu)
2. Press `1` (send command)
3. Type: `TEST_PACKET`
4. Press `ENTER`
5. Wait 10-15 seconds

**Expected Output:**
```
[DIAGNOSTIC] TEST_PACKET detected - monitoring sequence...
[RX] +CEREG: 0,1  (or 2,2 if searching)
[RX] +NETOPEN: 0
[RX] +CIPOPEN: 0,0
[RX] +CIPSEND: ...
[RX] +IPD... (if ACK received)
[DIAGNOSTIC] Sequence complete - analyzing logs...
[REPORT GENERATED] #001
  Status: HEALTHY (or FAILED/PARTIAL)
  File: reports/Network_Report_..._#001.pdf
```

### 5. Check the PDF Report
**Steps:**
1. Open File Explorer
2. Navigate to: `c:\document\MRS-BLE-Scanner-V0.1.2\MRS BLE Scanner V0.2\reports\`
3. Open the latest PDF file

**Expected Content:**
```
┌─────────────────────────────────────────────────┐
│ MRS NB-IoT Network Diagnostic Report           │
├─────────────────────────────────────────────────┤
│ Device IMEI: 351469520520687                    │
│ Timestamp: 2026-02-12 15:45:00                  │
│ Overall Status: ✅ HEALTHY                      │
├─────────────────────────────────────────────────┤
│ Layer-by-Layer Analysis:                        │
│   Layer 1: SIM        ✅ PASS                   │
│   Layer 1: IMSI       ℹ️ INFO (not visible)     │
│   Layer 2: Registration ✅ PASS                 │
│   Layer 3: PDP        ✅ PASS                   │
│   Layer 4: UDP        ✅ PASS                   │
│   Layer 4: ACK        ✅ RECEIVED               │
├─────────────────────────────────────────────────┤
│ Root Cause:                                     │
│   "Device is operating normally"                │
├─────────────────────────────────────────────────┤
│ Recommended Actions:                            │
│   • All systems operating normally              │
│   • ℹ️ IMSI not visible in logs                 │
│     (normal for some NB-IoT SIMs)               │
└─────────────────────────────────────────────────┘
```

### 6. Manual Report Generation (Optional)
**Purpose:** Generate a report on-demand without TEST_PACKET

**Steps:**
1. Press `Ctrl+P` (opens menu)
2. Press `4` (Generate diagnostic report NOW)
3. Wait 2 seconds

**Expected:** New PDF created with incremented number (#002, #003, etc.)

### 7. Toggle Auto-Report (Optional)
**Purpose:** Control whether reports are auto-generated after TEST_PACKET

**Steps:**
1. Press `Ctrl+P` (opens menu)
2. Press `5` (Toggle auto-report)
3. Current status will be shown

**Expected:** 
```
[CONFIG] Auto-report enabled
(or)
[CONFIG] Auto-report disabled
```

### 8. Exit
**Steps:**
1. Press `Ctrl+C` (exit)

**Expected:**
```
[STATS]
  Messages received: XX
  Reports generated: X
[EXIT] Goodbye
```

---

## Keyboard Controls Reference

| Key | Action |
|-----|--------|
| `Ctrl+P` | Open menu |
| `Ctrl+C` | Exit program |
| `1` (in menu) | Send command |
| `2` (in menu) | HTTP forwarding |
| `3` (in menu) | Toggle CR+LF |
| `4` (in menu) | Generate report NOW |
| `5` (in menu) | Toggle auto-report |
| `6` (in menu) | Back to receive mode |
| `7` (in menu) | Quit |

---

## Common Test Scenarios

### Scenario A: Device in Good Coverage
```
1. Send: NB_SHOW
2. Send: TEST_PACKET
3. Expected: HEALTHY status
4. Expected layers: All ✅ PASS
5. Expected ACK: ✅ RECEIVED
```

### Scenario B: Device Searching for Network
```
1. Send: NB_SHOW
2. Send: TEST_PACKET
3. Expected: FAILED status
4. Expected: Layer 2 ❌ FAIL (CEREG: 2,2)
5. Recommendation: "Move to better coverage"
```

### Scenario C: No Server Response
```
1. Send: NB_SHOW
2. Send: TEST_PACKET
3. Expected: PARTIAL status
4. Expected: Layers 1-4 ✅ PASS
5. Expected ACK: ⚠️ NONE
6. Recommendation: "Check server logs"
```

---

## Troubleshooting

### Issue: "No report generated after TEST_PACKET"
**Solutions:**
1. Check auto-report is ON (Ctrl+P → 5)
2. Verify NB_SHOW was sent first
3. Wait 15 seconds after TEST_PACKET
4. Try manual report (Ctrl+P → 4)

### Issue: "Report shows FAILED but device is working"
**Check:**
1. Did you send NB_SHOW first?
2. Is IMSI the only failure?
3. Look for the info note about IMSI
4. Check if ACK was received (Layer 4)

### Issue: "Can't open menu with Ctrl+P"
**Solutions:**
1. Make sure you're in RECEIVE MODE
2. Try pressing Ctrl+P multiple times
3. Check terminal is focused
4. Restart scanner if needed

---

## Expected Files After Testing

```
reports/
├── Network_Report_20260212_154500_#001.pdf  ← First test
├── Network_Report_20260212_154530_#002.pdf  ← Second test
└── Network_Report_20260212_154600_#003.pdf  ← Third test
```

Each report is:
- **Timestamped** (date + time)
- **Numbered** (#001, #002, #003...)
- **Self-contained** (all diagnostic info in one PDF)
- **Shareable** (can email to support team)

---

## Success Checklist

After testing, verify:
- [ ] Scanner connects to dustbin sensor
- [ ] NB_SHOW enables detailed logs
- [ ] TEST_PACKET triggers auto-report
- [ ] PDF appears in reports/ folder
- [ ] PDF opens without errors
- [ ] Report shows accurate status
- [ ] IMSI note appears (if applicable)
- [ ] Recommendations are clear
- [ ] Manual report works (Ctrl+P → 4)
- [ ] Auto-report toggle works (Ctrl+P → 5)

**All checked?** ✅ Your V0.2 is working perfectly!

---

**Quick Test (30 seconds):**
```
1. Launch → Select sensor → Wait for connection
2. Ctrl+P → 1 → NB_SHOW → ENTER
3. Ctrl+P → 1 → TEST_PACKET → ENTER
4. Wait 15 seconds
5. Open reports/ folder → Check PDF
```

**Done!** 🎉
