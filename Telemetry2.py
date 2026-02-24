import csv
import time
import smbus
import board
import busio
import adafruit_bmp3xx
import serial
# import bmp390cmds
# import gpscmds
# import mpu6050cmds



# ---- Conversions ----
accLSB_to_force = 16384
gyroLSB_to_dps = 131
pressure_oversampling = 8
temperature_oversampling = 2    
sea_level_pressure = 1013.25  # hPa (adjust for your location)

def setup():
    IMU_Setup()
    Barrometer_Setup()
    GPS_Setup()

def IMU_Setup():
    MPU6050_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43
    # Initialize I2C bus
    bus = smbus.SMBus(1)
    # Wake up MPU-6050 (it starts in sleep mode)
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def GPS_Setup():
    ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    timeout=1
)

def Barrometer_Setup():
    # Create I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create BMP390 sensor object
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

def Read_IMU():
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_XOUT_H + 2)
    acc_z = read_raw_data(ACCEL_XOUT_H + 4)

        # Read gyroscope data
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_XOUT_H + 2)
    gyro_z = read_raw_data(GYRO_XOUT_H + 4)

        # Convert to physical units
        # Accelerometer: ±2g → 16384 LSB/g
    ax = acc_x / accLSB_to_force 
    ay = acc_y / accLSB_to_force 
    az = acc_z / accLSB_to_force 
        # Gyroscope: ±250°/s → 131 LSB/(°/s)
    gx = gyro_x / gyroLSB_to_dps
    gy = gyro_y / gyroLSB_to_dps
    gz = gyro_z / gyroLSB_to_dps
    return ax, ay, az, gx, gy, gz

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)

    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value

def Read_Barrometer():

    temp= bmp.temperature
    press = bmp.pressure
    alt = bmp.altitude
    return temp,press,alt
    
def Read_GPS():
    line = ser.readline().decode('ascii', errors='replace').strip()
    line = gpscmds.line
    clock = []
    lat = []
    lon = []
    return clock,lat,lon

def Read_Data():
    IMU_Data = Read_IMU()
    Barrometer_Data = Read_Barrometer()
    GPS_Data = Read_GPS()
    data = [IMU_Data,Barrometer_Data,GPS_Data]
    return data

def Write_Data():
        with open('Telemetry.csv','a') as csvfile:
            csvfile.write(f"{data}\n")
        print("done Telemetry\n")

# --- Main Code ---
setup() # should be called in a different function but for testing purposes it's here

data = Read_Data()

