# USB-room-temperature-monitoring-with-MSP430G2553-and-Python-GUI-wxpython-
The project is a real time room temperature monitoring USB device that displays the temperature values on a python GUI app
It uses an MSP430G2553 microcontroller and a USB to TTL converter from silicon labs 
The python app requires THREADING to work since it has two major functions ie one that updates the values at the GUI side and one keeps checking for the data coming from the USB device using PYSERIAL module
The project can be upgraded for any thing that may require real time monitoring of different conditions such as industrial machines eg motor RPM , pressure , current drain , air quality etc
