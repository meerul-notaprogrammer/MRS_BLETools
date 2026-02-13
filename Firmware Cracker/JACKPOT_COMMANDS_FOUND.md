# 🎉 **JACKPOT - COMPLETE COMMAND SET DISCOVERED!**

## 🔥 **CRITICAL DISCOVERY**

The `?` command revealed **ALL 59 COMMANDS**!

---

## 🎯 **SERVER CONFIGURATION COMMANDS (FOUND!)**

### **25. SET_IP** ← **CHANGE SERVER IP!**
### **26. SET_PORT** ← **CHANGE SERVER PORT!**

---

## 📋 **COMPLETE COMMAND LIST**

### Configuration & System
```
0. ?                    ← Help menu
11. SYS_RESET          ← System reset
12. SYS_INFO           ← System information
21. COTA_CFG           ← COTA configuration
25. SET_IP             ← **SET SERVER IP**
26. SET_PORT           ← **SET SERVER PORT**
27. SET_ALIVE          ← Set alive interval
28. SET_SENSOR         ← Sensor configuration
```

### Sensor Commands
```
13. SENSOR_SHOW        ← Show sensor status
14. READ_SET           ← Read settings
29. S1_DEPTH           ← Sensor 1 depth
30. S2_DEPTH           ← Sensor 2 depth
31. SET_S_MON          ← Set sensor monitoring
32. SET_S_RCNT         ← Set sensor count
39. DISTANCE           ← Get distance
40. 6AXIS_RESET        ← Reset IMU
41. SENSOR_RESET       ← Reset sensors
52. S1_DIS_LV          ← Sensor 1 distance level
53. S2_DIS_LV          ← Sensor 2 distance level
```

### Network & Communication
```
16. UART_SHOW          ← Show UART status
17. UART_SEND=         ← Send via UART
18. FORCE_ALIVE        ← Force alive packet
20. FORCE_ATTACH       ← Force network attach
42. LORA_SHOW          ← Show LoRa status
43. NB_SHOW            ← **Show NB-IoT status**
```

### Power & Sleep
```
33. PD_START           ← Power down start
34. PD_6AXIS           ← Power down 6-axis
35. PD_TX              ← Power down TX
36. PD_SLEEP           ← Power down sleep
37. SYS_OPEN           ← System open
38. SYS_SLEEP          ← System sleep
```

### Data & Reporting
```
15. TIMESTAMP?         ← Get timestamp
19. FIFO_SHOW          ← Show FIFO buffer
22. DATE:              ← Set date
23. TIME:              ← Set time
24. NOW                ← Current time
49. TEST_PACKET        ← Send test packet
50. RP_FG              ← Report flag
51. REPORT             ← Generate report
48. SEND_VREC          ← Send voltage record
```

### Diagnostics
```
44. VOLTAGE            ← Battery voltage
45. DIS_KEEP           ← Distance keep
46. VOL_RECORD         ← Voltage record
47. VOL_CLEAR          ← Clear voltage record
54. DETECT_MODE        ← Detection mode
55. KEEP_DETECT        ← Keep detection
56. BL_NAME            ← Bluetooth name
57. COVER_CHK          ← Cover check
58. COVER_ALARM        ← Cover alarm
59. SELECT_DETECT      ← Select detection
```

---

## 🚀 **HOW TO CHANGE SERVER**

### Step 1: Get Current Configuration
```
Send via BLE:
NB_SHOW              ← Shows current NB-IoT config (IP, port, etc.)
```

### Step 2: Set New Server IP
```
Send via BLE:
SET_IP 192.168.1.100    ← Your server IP
```

### Step 3: Set New Server Port
```
Send via BLE:
SET_PORT 8080           ← Your server port
```

### Step 4: Verify
```
Send via BLE:
NB_SHOW              ← Verify new configuration
```

### Step 5: Force Update
```
Send via BLE:
FORCE_ATTACH         ← Force reconnect to new server
TEST_PACKET          ← Send test packet to verify
```

---

## 🚀 **TRY THIS NOW!**

```bash
# Run Scanner.py
cd "MRS BLE Scanner V0.2"
python Scanner.py

# Connect to sensor
# Press 'c' for command mode
# Send these commands:

?              # See all commands
NB_SHOW        # See current server
SET_IP 192.168.1.100
SET_PORT 8080
NB_SHOW        # Verify change
TEST_PACKET    # Test
```

---

**🎉 WE FOUND THE CONFIGURATION INTERFACE!**

**Commands 25 & 26 are exactly what we need: SET_IP and SET_PORT!**
