# ----Setup----
#Enable I²C:
#sudo raspi-config → Interfacing Options → I2C → Enable

#Install dependencies:
#sudo apt-get install python3-smbus

#Save the script (e.g., ups_monitor.py) and run:
#python3 ups_monitor.py

#!/usr/bin/python3
import smbus
import time

# I2C address of INA219
INA219_ADDR = 0x42

# Register addresses
BUS_VOLTAGE_REG = 0x02
SHUNT_VOLTAGE_REG = 0x01
CURRENT_REG = 0x04
CALIBRATION_REG = 0x05

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_voltage():
    # Read 2 bytes from bus voltage register
    data = bus.read_i2c_block_data(INA219_ADDR, BUS_VOLTAGE_REG, 2)
    # Convert to volts (LSB = 4mV)
    voltage = (data[0] << 3) | (data[1] >> 5)
    return voltage * 0.004

def read_current():
    # Read from current register
    data = bus.read_i2c_block_data(INA219_ADDR, CURRENT_REG, 2)
    # Convert to mA (assumes calibration for ±2A)
    current = (data[0] << 8) | data[1]
    if current > 32767:
        current -= 65536  # Sign bit handling
    return current * 0.1  # LSB = 0.1mA

def calculate_battery_percent():
    voltage = read_voltage()
    # Assuming 2S Li-ion: 8.4V (full) to 6.0V (empty)
    if voltage >= 8.4:
        return 100.0
    elif voltage <= 6.0:
        return 0.0
    else:
        return ((voltage - 6.0) / (8.4 - 6.0)) * 100


bus_voltage = read_voltage()
current = read_current()
charge = calculate_battery_percent()