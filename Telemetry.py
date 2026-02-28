import csv
import time
import smbus
import board
import busio
import adafruit_bmp3xx
import serial
import control as con
# import bmp390cmds
# import gpscmds
# import mpu6050cmds
# ---- Conversions ---- 
accLSB_to_force = 16384
gyroLSB_to_dps = 131
pressure_oversampling = 8
temperature_oversampling = 2    
sea_level_pressure = 1013.25  # hPa (adjust for your location)


class Telemetry:

    def Read_IMU(self,ACCEL_XOUT_H,GYRO_XOUT_H):
        acc_x = self.read_raw_data(con.ACCEL_XOUT_H)
        acc_y = self.read_raw_data(con.ACCEL_XOUT_H + 2)
        acc_z = self.read_raw_data(con.ACCEL_XOUT_H + 4)

            # Read gyroscope data
        gyro_x = self.read_raw_data(con.GYRO_XOUT_H)
        gyro_y = self.read_raw_data(con.GYRO_XOUT_H + 2)
        gyro_z = self.read_raw_data(con.GYRO_XOUT_H + 4)

            # Convert to physical units
            # Accelerometer: ±2g → 16384 LSB/g
        self.ax = acc_x / accLSB_to_force 
        self.ay = acc_y / accLSB_to_force 
        self.az = acc_z / accLSB_to_force 
            # Gyroscope: ±250°/s → 131 LSB/(°/s)
        self.gx = gyro_x / gyroLSB_to_dps
        self.gy = gyro_y / gyroLSB_to_dps
        self.gz = gyro_z / gyroLSB_to_dps
        return self.ax,self.ay,self.az,self.gx,self.gy,self.gz

    def read_raw_data(self,addr):
        high = con.bus.read_byte_data(con.MPU6050_ADDR, addr)
        low = con.bus.read_byte_data(con.MPU6050_ADDR, addr + 1)

        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def Read_Barrometer(self):
        self.temp= con.bmp.temperature
        self.press = con.bmp.pressure
        self.alt = con.bmp.altitude
        return self.temp,self.press,self.alt
    def Read_GPS(self):
        line = con.ser.readline().decode('ascii', errors='replace').strip()
        clock = []
        lat = []
        lon = []
        return clock,lat,lon

    def Read_Data(self):
        IMU_Data = self.Read_IMU(con.ACCEL_XOUT_H,con.GYRO_XOUT_H)
        Barrometer_Data = self.Read_Barrometer()
        GPS_Data = self.Read_GPS()
        data = [IMU_Data,Barrometer_Data,GPS_Data]
        return data

def Write_Data():
        with open('Telemetry.csv','a') as csvfile:
            csvfile.write(f"{data}\n")
        print("done Telemetry\n")

tel = Telemetry()
data = tel.Read_Data()

Write_Data()
