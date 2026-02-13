# QuickServer - MRS BLE Scanner

## 🚀 Quick Start

Simply **double-click `Start.bat`** to run the local server!

## 📋 What This Does

The QuickServer starts two services:

1. **Web Dashboard** - http://localhost:5000
   - Real-time sensor data visualization
   - Packet monitoring
   - Server configuration display

2. **UDP Server** - Port 8081
   - Receives sensor data from NB-IoT devices
   - Logs all incoming packets

## 🔧 How to Use

1. **Start the Server**
   - Double-click `Start.bat`
   - Wait for the server to start (you'll see green text)

2. **Open the Dashboard**
   - Open your browser
   - Go to: http://localhost:5000

3. **Configure Your Sensor**
   - Use Scanner.py to connect to your sensor
   - Send these commands:
     ```
     SET_IP <your_local_ip>
     SET_PORT 8081
     TEST_PACKET
     ```

4. **View Data**
   - Watch the dashboard update in real-time
   - Check the terminal for detailed packet logs

## 📁 Files Included

- `Start.bat` - Quick start script
- `TestServer.py` - Main server application
- `dashboard.html` - Web dashboard interface
- `README.md` - This file

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal window to stop the server.

## 📝 Notes

- Make sure Python is installed and in your PATH
- The server will create a `sensor_data_log.txt` file for logging
- Dashboard auto-refreshes every 2 seconds
