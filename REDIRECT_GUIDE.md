# 🚀 **REDIRECT SENSOR TO YOUR SERVER - STEP BY STEP**

## ✅ **SERVER IS RUNNING!**

Your local UDP server is now running on:
- **IP:** Check the server output for your local IP
- **Port:** 8080
- **Protocol:** UDP

---

## 📋 **STEP-BY-STEP GUIDE**

### Step 1: Keep Server Running
The server is already running in the background. You'll see packets appear when sensor sends data.

### Step 2: Open Scanner.py in NEW Terminal
```bash
# Open a NEW terminal/command prompt
cd "c:\document\MRS-BLE-Scanner-V0.1.2\MRS BLE Scanner V0.2"
python Scanner.py
```

### Step 3: Connect to Sensor
1. Scanner will scan for BLE devices
2. Select your sensor: **N_01E1_N6BR1_162464**
3. Wait for connection

### Step 4: Enter Command Mode
- Press **'c'** to enter command mode

### Step 5: Check Current Server
Send this command:
```
NB_SHOW
```

This will show you the current server IP and port.

### Step 6: Get Your Local IP
Look at the TestServer.py output - it shows your local IP.

Example: `192.168.1.100` or `10.0.0.5`

### Step 7: Redirect to Your Server
Send these commands one by one:

```
SET_IP 192.168.1.100
```
(Replace with YOUR local IP from Step 6)

```
SET_PORT 8080
```

### Step 8: Verify Configuration
```
NB_SHOW
```

Check if IP and port changed to your values.

### Step 9: Test Connection
```
TEST_PACKET
```

This sends a test packet to your server.

### Step 10: Force Reconnect
```
FORCE_ATTACH
```

This forces the sensor to reconnect to the new server.

---

## 🎯 **WHAT TO EXPECT**

### In TestServer.py Window:
You should see:
```
================================================================================
[PACKET #1] 2026-02-13 16:10:00
================================================================================

[SOURCE]
  IP: 10.xxx.xxx.xxx
  Port: xxxxx

[RAW DATA]
  Size: XX bytes
  Hex: 0654351469520520687041006698...
  
[PARSED DATA]
  possible_imei: 351469520687041
  packet_length: XX
```

### In Scanner.py Window:
You might see responses like:
```
OK
+CIPOPEN: 0,0
```

---

## 🔍 **TROUBLESHOOTING**

### No packets received?
1. Check if sensor accepted commands (look for "OK" response)
2. Try `FORCE_ATTACH` again
3. Try `TEST_PACKET` again
4. Check firewall isn't blocking port 8080

### Commands not working?
1. Make sure you're in command mode (pressed 'c')
2. Try sending `?` first to see if commands work
3. Commands might need specific format (try with/without spaces)

### Wrong IP?
1. Make sure you used YOUR local IP, not the example
2. Check TestServer.py output for correct IP
3. Use `ipconfig` (Windows) or `ifconfig` (Linux) to find your IP

---

## 📊 **COMMAND REFERENCE**

| Command | Purpose | Example |
|---------|---------|---------|
| `?` | Show all commands | `?` |
| `NB_SHOW` | Show NB-IoT config | `NB_SHOW` |
| `SET_IP` | Set server IP | `SET_IP 192.168.1.100` |
| `SET_PORT` | Set server port | `SET_PORT 8080` |
| `TEST_PACKET` | Send test packet | `TEST_PACKET` |
| `FORCE_ATTACH` | Force reconnect | `FORCE_ATTACH` |
| `SYS_INFO` | System info | `SYS_INFO` |
| `SENSOR_SHOW` | Sensor status | `SENSOR_SHOW` |

---

## 🎉 **SUCCESS INDICATORS**

### ✅ Server Configured Successfully:
- `NB_SHOW` shows your IP and port
- `TEST_PACKET` triggers packet in TestServer.py
- Regular sensor data appears in TestServer.py

### ✅ Data Flowing:
- Packets appear every few minutes
- Packet count increases
- `sensor_data_log.txt` file grows

---

## 📝 **DATA LOGGING**

All received packets are logged to:
```
c:\document\MRS-BLE-Scanner-V0.1.2\sensor_data_log.txt
```

You can review this file to see all received data.

---

## 🚀 **NEXT STEPS AFTER SUCCESS**

1. **Analyze Data Format**
   - Review received packets
   - Decode the protocol
   - Parse sensor values

2. **Build Proper Server**
   - Parse and store data in database
   - Create web dashboard
   - Set up alerts

3. **Deploy to Cloud**
   - Use your VPS
   - Set up public IP
   - Configure sensor to use cloud server

---

## ⚠️ **IMPORTANT NOTES**

### Persistence
- Settings might reset after sensor reboot
- You may need to reconfigure after power cycle
- Test if settings persist

### Network
- Sensor uses NB-IoT cellular network
- Your server must be reachable from internet for production
- For testing, local network is fine if sensor is on same network

### Firewall
- Make sure port 8080 is open
- Windows Firewall might block it
- Add exception if needed

---

## 🎯 **QUICK COMMAND SEQUENCE**

```bash
# In Scanner.py (after connecting):
c                    # Enter command mode
?                    # List commands
NB_SHOW             # Check current server
SET_IP 192.168.1.100    # Your local IP
SET_PORT 8080       # Your port
NB_SHOW             # Verify
TEST_PACKET         # Test
FORCE_ATTACH        # Force reconnect
```

---

**🚀 YOUR SERVER IS READY! NOW REDIRECT THE SENSOR!**
