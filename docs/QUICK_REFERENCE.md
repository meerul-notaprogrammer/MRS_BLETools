# 🚀 MRS BLE Scanner V0.2 - Quick Reference

## 📋 One-Page Cheat Sheet

### 🎯 Quick Start (30 seconds)
```bash
1. Double-click Start.bat
2. Press Y (agree)
3. Press ENTER (skip HTTP)
4. Wait for scan
5. Type device number
6. You're connected!
```

### ⌨️ Essential Commands

| Command | What It Does |
|---------|-------------|
| `NB_SHOW` | Enable detailed AT command logs |
| `TEST_PACKET` | Send test packet + auto-generate PDF report |
| `SYS_INFO` | Get device information |
| `DISTANCE` | Read sensor distances |
| `SYS_RESET` | Restart sensor (disconnects BLE) |

### 🎮 Keyboard Controls

| Key | Action |
|-----|--------|
| `Ctrl+P` | Open menu |
| `Ctrl+C` | Exit program |

### 📊 Understanding Reports

#### Status Indicators
| Symbol | Meaning |
|--------|---------|
| ✅ HEALTHY | All systems working |
| ⚠️ PARTIAL | Sent but no server ACK |
| ❌ FAILED | Something is broken |

#### Common Failure Layers
| Layer | Problem | Quick Fix |
|-------|---------|-----------|
| Layer 1: SIM | SIM not ready | Check SIM card insertion |
| Layer 2: Registration | CEREG: 2,2 | Move to better coverage |
| Layer 3: PDP | NETOPEN failed | Check APN settings |
| Layer 4: UDP | No ACK | Check server status |

### 🔧 Troubleshooting Decision Tree

```
Device not sending data?
│
├─ Is SIM Ready? (Check report Layer 1)
│  ├─ NO → Reinsert SIM card
│  └─ YES ↓
│
├─ Is CEREG registered? (Check report Layer 2)
│  ├─ NO (CEREG: 2,2) → Move to better coverage
│  ├─ NO (CEREG: 0,3) → Contact carrier (IMEI blocked?)
│  └─ YES ↓
│
├─ Did NETOPEN succeed? (Check report Layer 3)
│  ├─ NO → Check APN: m2mxnbiot
│  └─ YES ↓
│
├─ Did CIPOPEN succeed? (Check report Layer 4)
│  ├─ NO → Check network connectivity
│  └─ YES ↓
│
├─ Was packet sent? (Check report Layer 4)
│  ├─ NO → Check signal quality (RSRP/SNR)
│  └─ YES ↓
│
└─ Did you get ACK? (Check report Layer 4)
   ├─ NO → Check server (UDP = no guarantee)
   └─ YES → ✅ Everything working!
```

### 📡 Signal Quality Quick Guide

#### RSRP (Signal Power)
| Value | Quality | Action |
|-------|---------|--------|
| -70 to -85 dBm | ✅ Excellent | None needed |
| -85 to -95 dBm | ✅ Good | None needed |
| -95 to -105 dBm | ⚠️ Weak | Consider moving |
| < -110 dBm | ❌ Poor | Move to better location |

#### SNR (Signal-to-Noise)
| Value | Quality | Action |
|-------|---------|--------|
| > 5 dB | ✅ Excellent | None needed |
| 0 to 5 dB | ✅ Good | None needed |
| -5 to 0 dB | ⚠️ Marginal | Monitor |
| < -10 dB | ❌ Poor | Move to better location |

### 📁 File Locations

```
MRS BLE Scanner V0.2/
├── Start.bat           ← Double-click to start
├── Scanner.py          ← Main program
├── README.txt          ← Full documentation
└── reports/            ← Your PDF reports here
    ├── Network_Report_093982_..._#001.pdf
    ├── Network_Report_093982_..._#002.pdf
    └── ...
```

### 🎯 Common Workflows

#### Workflow 1: First Time Setup
```
1. Start.bat
2. Agree to terms
3. Skip HTTP (press ENTER)
4. Select device
5. Send: NB_SHOW
6. Send: TEST_PACKET
7. Check reports/ folder
```

#### Workflow 2: Quick Health Check
```
1. Connect to device
2. Ctrl+P → 1 → TEST_PACKET
3. Wait 10 seconds
4. Open latest PDF in reports/
5. Check overall status
```

#### Workflow 3: Troubleshooting
```
1. Connect to device
2. Send: NB_SHOW (enable logs)
3. Send: TEST_PACKET
4. Open PDF report
5. Go to "Root Cause Analysis"
6. Follow "Recommended Actions"
7. Send TEST_PACKET again
8. Compare new report
```

### 🔄 CEREG Status Codes (Most Important!)

| Code | Meaning | What To Do |
|------|---------|------------|
| 0,1 | ✅ Registered (Home) | Perfect! |
| 0,5 | ✅ Registered (Roaming) | Perfect! |
| 2,2 | ❌ Searching | Move to better coverage |
| 0,3 | ❌ Registration Denied | Call carrier |
| 0,0 | ❌ Not Registered | Check SIM |

### 💡 Pro Tips

1. **Always enable NB_SHOW first**
   ```
   Ctrl+P → 1 → NB_SHOW
   ```
   This gives you detailed logs for better diagnostics.

2. **Compare reports over time**
   ```
   reports/
   ├── #001.pdf  (FAILED - Searching)
   ├── #002.pdf  (FAILED - Searching)
   ├── #003.pdf  (HEALTHY - Success!)  ← What changed?
   ```

3. **Check signal quality trends**
   - If RSRP is consistently < -100, consider antenna upgrade
   - If SNR is consistently < 0, check for interference

4. **Use manual report generation**
   ```
   Ctrl+P → 5 → Toggle auto-report OFF
   Ctrl+P → 4 → Generate report NOW
   ```
   Useful when you want to capture specific moments.

5. **Keep reports for warranty claims**
   - PDF reports are professional documentation
   - Show carrier if device issues persist
   - Prove network coverage problems

### ⚠️ Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Not enabling NB_SHOW | Limited diagnostic info | Always send NB_SHOW first |
| Ignoring signal quality | Weak signal = failures | Check RSRP/SNR in reports |
| Testing indoors | Poor NB-IoT coverage | Test outdoors or near window |
| Wrong APN | PDP context fails | Must be: m2mxnbiot |
| Expecting instant registration | CEREG takes time | Wait 2-3 minutes |

### 📞 When To Contact Support

Contact technical support if:
- ✅ SIM Ready
- ✅ IMSI visible
- ❌ CEREG: 0,3 (Registration Denied) repeatedly
- ❌ Good signal (RSRP > -95) but still failing

Attach your PDF reports to support ticket!

### 🎓 Learning Path

#### Beginner
1. Understand the 4 layers (SIM → Registration → PDP → UDP)
2. Learn to read PDF report status
3. Follow recommended actions

#### Intermediate
4. Understand CEREG codes
5. Interpret signal quality (RSRP/SNR)
6. Recognize AT command patterns

#### Advanced
7. Read raw AT command logs
8. Predict failures before they happen
9. Optimize antenna placement using signal data

### 📚 Additional Resources

- `README.txt` - Full documentation
- `UPGRADE_SUMMARY.md` - Technical details
- `COMPARISON.md` - V0.1 vs V0.2 differences
- Sensor Diagnostics Skill - Complete knowledge base

### 🆘 Emergency Quick Fixes

#### "Device won't connect via BLE"
```
1. Shake/tap sensor to wake it
2. Wait 5 seconds
3. Scan again
```

#### "CEREG stuck at 2,2"
```
1. Move device outdoors
2. Wait 3 minutes
3. Send TEST_PACKET again
```

#### "Reports not generating"
```
1. Check reports/ folder exists
2. Ctrl+P → 5 (check auto-report is ON)
3. Try manual: Ctrl+P → 4
```

#### "Can't understand report"
```
1. Look at "Overall Status" (top)
2. Find first ❌ in layer table
3. Read "Recommended Actions"
4. Do the first action
5. Test again
```

---

**Remember:** The PDF reports are your friend! They translate technical jargon into plain English and tell you exactly what to do.

**Pro Tip:** Print this page and keep it next to your computer! 📄
