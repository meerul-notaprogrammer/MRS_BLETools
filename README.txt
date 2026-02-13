MRS BLE Scanner Tool V0.1.2
Professional Scan, Read, Command, Post using BLE and HTTP

Requirements
- Windows 10/11
- Python 3.8+ (auto-installed if missing)

Quick Start
1. Open Start.bat
2. Answer User Agreement
3. Enter API URL (or press ENTER to skip)
4. Shake or tap the sensor to enter Bluetooth mode
5. Select device number from the scan results

Controls
Ctrl+P = Open command menu
Ctrl+C = End program

Menu (Ctrl+P) listed below:
1. Send command to sensor
2. Enable/disable HTTP forwarding
3. Toggle CR+LF
4. Back to receive mode
5. Quit

Sensor Commands
- SYS_RESET   = Reset sensor (sensor restart it will disconnect BLE)
- SYS_OPEN    = Open receiving mode (sensor restart it will disconnect BLE)
- SYS_SLEEP   = Sleep mode (sensor will disconnect BLE)
- SYS_INFO    = Get sensor info
- S1_DEPTH    = Set actual depth main sensor (in cm)
- S2_DEPTH    = Set actual depth secondary sensor (in cm) #in TRX Case this will be not used
- NB_SHOW     = Show system info enable/disable
- TEST_PACKET = Test packet 06
- DISTANCE    = Built-in distance sensor readings

Package Contents
- Start.bat  = Auto-launcher script
- Scanner.py = Main application
- README.md  = This file