# 🎯 MRS BLE Scanner V0.2 - Diagnostic Logic Flow

## Simple Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│  TEST_PACKET Sequence Detected                              │
│  Analyzing logs...                                           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Did server ACK?    │
                    └──────────┬──────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                YES                       NO
                 │                         │
                 ▼                         ▼
        ┌────────────────┐      ┌──────────────────┐
        │  ✅ HEALTHY    │      │  Was data sent?  │
        │                │      └────────┬─────────┘
        │  Status: OK    │               │
        │  Layers: 2-4   │      ┌────────┴────────┐
        │  (No SIM check)│      │                 │
        └────────────────┘     YES               NO
                                │                 │
                                ▼                 ▼
                       ┌────────────────┐  ┌──────────────────┐
                       │  ⚠️ PARTIAL    │  │  Did register?   │
                       │                │  └────────┬─────────┘
                       │  Status: Sent  │           │
                       │  Layers: 2-4   │  ┌────────┴────────┐
                       │  (No SIM check)│  │                 │
                       │  Note: No ACK  │ YES               NO
                       └────────────────┘  │                 │
                                           ▼                 ▼
                                  ┌────────────────┐  ┌──────────────────┐
                                  │  ❌ FAILED     │  │  Is SIM ready?   │
                                  │                │  └────────┬─────────┘
                                  │  Layer 2 FAIL  │           │
                                  │  Show SIM+IMSI │  ┌────────┴────────┐
                                  │  (for diagnosis)│  │                 │
                                  └────────────────┘ YES               NO
                                                      │                 │
                                                      ▼                 ▼
                                             ┌────────────────┐  ┌──────────────────┐
                                             │  ❌ FAILED     │  │  ❌ FAILED       │
                                             │                │  │                  │
                                             │  Layer 2 FAIL  │  │  Layer 1 FAIL    │
                                             │  (Registration)│  │  (SIM not ready) │
                                             └────────────────┘  └──────────────────┘
```

---

## Key Principles

### 1. **Success First**
```
IF (ACK received OR data sent):
    → Device is working!
    → Skip SIM/IMSI checks
    → Report HEALTHY or PARTIAL
```

### 2. **Diagnose Failures Only When Needed**
```
IF (nothing worked):
    → Check why it failed
    → Show SIM/IMSI status (for diagnosis)
    → Provide specific recommendations
```

### 3. **No Confusion**
```
Working device = Clean report (no SIM/IMSI rows)
Failed device = Full diagnosis (show all layers)
```

---

## Report Examples

### Example 1: Perfect Success (ACK Received)

**Input:** TEST_PACKET sent, server responds with ACK

**Output:**
```
┌─────────────────────────────────────────────────┐
│ Overall Status: ✅ HEALTHY                      │
├─────────────────────────────────────────────────┤
│ Layer-by-Layer Analysis:                        │
│   Layer 2: Registration  ✅ PASS                │
│   Layer 3: PDP Context   ✅ PASS                │
│   Layer 4: UDP Socket    ✅ PASS                │
│   Layer 4: Data Send     ✅ PASS (20 bytes)     │
│   Layer 4: Server ACK    ✅ RECEIVED            │
├─────────────────────────────────────────────────┤
│ Root Cause:                                     │
│   "Device is operating normally - server        │
│    acknowledged data transmission"              │
├─────────────────────────────────────────────────┤
│ Recommendations:                                │
│   • All systems operating normally              │
│   • Data successfully transmitted and           │
│     acknowledged                                │
└─────────────────────────────────────────────────┘
```

**Note:** No SIM/IMSI rows! Device is clearly working.

---

### Example 2: Partial Success (Sent But No ACK)

**Input:** TEST_PACKET sent, but no server response

**Output:**
```
┌─────────────────────────────────────────────────┐
│ Overall Status: ⚠️ PARTIAL                      │
├─────────────────────────────────────────────────┤
│ Layer-by-Layer Analysis:                        │
│   Layer 2: Registration  ✅ PASS                │
│   Layer 3: PDP Context   ✅ PASS                │
│   Layer 4: UDP Socket    ✅ PASS                │
│   Layer 4: Data Send     ✅ PASS (20 bytes)     │
│   Layer 4: Server ACK    ⚠️ NONE                │
├─────────────────────────────────────────────────┤
│ Root Cause:                                     │
│   "Packet sent successfully but no server       │
│    acknowledgment received"                     │
├─────────────────────────────────────────────────┤
│ Recommendations:                                │
│   • Data was transmitted over NB-IoT network    │
│     successfully                                │
│   • Server may not have received packet         │
│     (UDP is connectionless)                     │
│   • Check server logs to verify packet arrival  │
│   • Verify server is online and responding      │
└─────────────────────────────────────────────────┘
```

**Note:** Still no SIM/IMSI rows! Device sent data successfully.

---

### Example 3: Registration Failed

**Input:** TEST_PACKET sent, but device cannot register

**Output:**
```
┌─────────────────────────────────────────────────┐
│ Overall Status: ❌ FAILED                       │
├─────────────────────────────────────────────────┤
│ Layer-by-Layer Analysis:                        │
│   Layer 1: SIM Card      ✅ PASS                │
│   Layer 1: IMSI          ⚠️ N/A                 │
│   Layer 2: Registration  ❌ FAIL (CEREG: 2,2)   │
│   Layer 3: PDP Context   ❌ FAIL                │
│   Layer 4: UDP Socket    ❌ FAIL                │
│   Layer 4: Data Send     ❌ FAIL                │
│   Layer 4: Server ACK    ⚠️ NONE                │
├─────────────────────────────────────────────────┤
│ Root Cause:                                     │
│   "Modem is searching for network but cannot    │
│    register (CEREG: 2,2)"                       │
├─────────────────────────────────────────────────┤
│ Recommendations:                                │
│   • Move device to area with better NB-IoT      │
│     coverage                                    │
│   • Check if NB-IoT service is available in     │
│     this area                                   │
│   • Verify SIM card has active NB-IoT plan      │
│   • Wait a few minutes and retry                │
└─────────────────────────────────────────────────┘
```

**Note:** NOW we show SIM/IMSI rows (for diagnosis). Device failed, so we need full details.

---

### Example 4: SIM Not Ready

**Input:** TEST_PACKET sent, but SIM not detected

**Output:**
```
┌─────────────────────────────────────────────────┐
│ Overall Status: ❌ FAILED                       │
├─────────────────────────────────────────────────┤
│ Layer-by-Layer Analysis:                        │
│   Layer 1: SIM Card      ❌ FAIL                │
│   Layer 1: IMSI          ❌ FAIL                │
│   Layer 2: Registration  ❌ FAIL                │
│   Layer 3: PDP Context   ❌ FAIL                │
│   Layer 4: UDP Socket    ❌ FAIL                │
│   Layer 4: Data Send     ❌ FAIL                │
│   Layer 4: Server ACK    ⚠️ NONE                │
├─────────────────────────────────────────────────┤
│ Root Cause:                                     │
│   "SIM card not detected or not ready"          │
├─────────────────────────────────────────────────┤
│ Recommendations:                                │
│   • Check if SIM card is properly inserted      │
│   • Verify SIM card is activated                │
│   • Try removing and reinserting SIM card       │
│   • Contact carrier to verify SIM status        │
└─────────────────────────────────────────────────┘
```

**Note:** Full diagnosis with SIM/IMSI details (device completely failed).

---

## Code Logic

### NetworkDiagnostics.py

```python
def _determine_status(self, ...):
    # PRIORITY 1: Check if device successfully communicated
    device_communicated = ack_received or cipsend_success
    
    if device_communicated:
        # Device is working! Skip SIM/IMSI checks entirely
        
        if ack_received:
            return ("HEALTHY", None, "Device operating normally", [...])
        
        elif cipsend_success:
            return ("PARTIAL", "Layer 4: Server Response", "Sent but no ACK", [...])
    
    # PRIORITY 2: Device didn't communicate - now check why
    
    if not sim_ready and not cereg_registered:
        return ("FAILED", "Layer 1: SIM", "SIM not ready", [...])
    
    if not cereg_registered:
        return ("FAILED", "Layer 2: Registration", "Cannot register", [...])
    
    # ... continue checking other layers
```

### PDFReportGenerator.py

```python
# Check if device successfully communicated
device_communicated = ack_received or cipsend_success

layer_data = [['Layer', 'Component', 'Status', 'Details']]

# Only show SIM/IMSI if device didn't communicate
if not device_communicated:
    layer_data.extend([
        ['1', 'SIM Card', '✅ PASS' if sim_ready else '❌ FAIL', ...],
        ['1', 'IMSI', '✅ PASS' if imsi else '⚠️ N/A', ...]
    ])

# Always show these layers
layer_data.extend([
    ['2', 'Registration', ...],
    ['3', 'PDP Context', ...],
    ['4', 'UDP Socket', ...],
    ['4', 'Data Send', ...],
    ['4', 'Server ACK', ...]
])
```

---

## Summary

### Simple Rules

1. **ACK received?** → ✅ HEALTHY (no SIM check)
2. **Data sent?** → ✅ HEALTHY or ⚠️ PARTIAL (no SIM check)
3. **Nothing worked?** → ❌ FAILED (show SIM for diagnosis)

### Why This Works

- **No confusion** - Working device = clean report
- **Focus on results** - Did data reach server?
- **Diagnose only when needed** - Show SIM only if failed
- **Clear recommendations** - What to do next

---

**This is the final, production-ready logic!** ✅
