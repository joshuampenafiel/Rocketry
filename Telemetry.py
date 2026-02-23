import csv
import bmp390cmds
import gpscmds
import mpu6050cmds
import time
#record data
line = gpscmds.line
clock = []
lat = []
lon = []

if line.startswith('$GNRMC'):
    parts = line.split(",")
    clock = parts[1]
    lat = parts[3] 
    lon = parts[5]              
    temp = bmp390cmds.temperature
    press = bmp390cmds.pressure
    alt = bmp390cmds.altitude
    gx = mpu6050cmds.gx
    gy = mpu6050cmds.gy
    gz = mpu6050cmds.gz
    ax = mpu6050cmds.ax
    ay = mpu6050cmds.ay
    az = mpu6050cmds.az
    data = [gx,gy,gz,ax,ay,az,temp,press,alt,lat,lon,clock]
    #open the csv
    with open('Telemetry.csv','a') as csvfile:
        csvfile.write(f"{data}\n")
print("done Telemetry\n")

class Telemetry:

    def self.__init__():
        self.ax =
        slef.ay = mpu6050cmds
        bus = smbus.SMBus(1)
        # Wake up MPU-6050 (it starts in sleep mode)
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)


    def readIMU():
            bus = smbus.SMBus(1)
            # Wake up MPU-6050 (it starts in sleep mode)
            bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
            read_raw_data

            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_XOUT_H + 2)
            acc_z = read_raw_data(ACCEL_XOUT_H + 4)

                    # Read gyroscope data
            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_XOUT_H + 2)
            gyro_z = read_raw_data(GYRO_XOUT_H + 4)

            # Convert to physical units
            # Accelerometer: ±2g → 16384 LSB/g
            ax = acc_x / 16384.0
            ay = acc_y / 16384.0
            az = acc_z / 16384.0
            # Gyroscope: ±250°/s → 131 LSB/(°/s)
            gx = gyro_x / 131.0
            gy = gyro_y / 131.0
            self.gz = gyro_z / 131.0


    def readBarometer():

        # get barometer data

        self.temp = baroTemp
        self.press = baroPress

    def writeToCSV():
        # pandas
        csvfile.write(f"{data}\n")
