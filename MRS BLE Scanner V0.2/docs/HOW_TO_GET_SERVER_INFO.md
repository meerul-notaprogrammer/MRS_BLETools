# 🔍 **HOW TO GET SERVER IP/PORT IN REPORT**

## ⚠️ **IMPORTANT**

The report you're looking at (`Network_Report_162464_20260213_175625_#001.pdf`) was generated **BEFORE** the server configuration feature was added.

**Timeline:**
- 17:56:25 - Report generated (old version)
- 17:48:00 - Server config feature added (new version)

**You need to generate a NEW report to see the server configuration!**

---

## 🚀 **STEP-BY-STEP: Get Server Info in Report**

### Step 1: Run Scanner.py
```bash
cd "c:\document\MRS-BLE-Scanner-V0.1.2\MRS BLE Scanner V0.2"
python Scanner.py
```

### Step 2: Connect to Sensor
- Select your sensor: **N_01E1_N6BR1_162464**
- Wait for connection

### Step 3: Enter Command Mode
Press: **`c`**

### Step 4: Send NB_SHOW (IMPORTANT!)
```
NB_SHOW
```

**This command captures the server configuration!**

Wait for response. You should see something like:
```
Server: 47.xxx.xxx.xxx:8080
APN: m2mxnbiot
Status: Connected
```

### Step 5: Send TEST_PACKET
```
TEST_PACKET
```

This will:
1. Test the network connection
2. Generate a NEW diagnostic report
3. **Include the server configuration** from NB_SHOW

### Step 6: Check the New Report
```
Location: MRS BLE Scanner V0.2/reports/
File: Network_Report_162464_YYYYMMDD_HHMMSS_#002.pdf
```

The NEW report will have the **🌐 Server Configuration** section!

---

## 📋 **Quick Command Sequence**

After connecting to sensor:

```
c              # Enter command mode
NB_SHOW        # Capture server config (WAIT for response!)
TEST_PACKET    # Generate report with server info
```

---

## ❓ **Why Isn't It in the Old Report?**

The old report was generated with the **old version** of the code that didn't extract server configuration.

**The feature was added AFTER your report was created.**

You need to generate a **NEW** report with the **updated code** to see the server configuration.

---

## 🎯 **What You'll See in the New Report**

```
🌐 Server Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Setting          Value
────────────────────────────────────────────────
Server IP        47.xxx.xxx.xxx
Server Port      8080
APN              m2mxnbiot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚡ **TL;DR**

1. **Old report** = No server config (feature didn't exist yet)
2. **New report** = Has server config (feature added now)
3. **Solution:** Run Scanner.py → Send `NB_SHOW` → Send `TEST_PACKET` → Get new report!

---

**🚀 RUN IT NOW TO GET THE SERVER INFO!**
