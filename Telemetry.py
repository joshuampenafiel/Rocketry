import csv
import bmp390
import gps
import mpu6050
import time
#record data
line = gps.line
lat = []
lon = []
while True:
    if line.startswith('$GNRMC'):
        parts = line.split(",")
        lat = parts[3] 
        lon = parts[5]              
    temp = bmp390.temperature
    press = bmp390.pressure
    alt = bmp390.altitude
    gx = mpu6050.gx
    gy = mpu6050.gy
    gz = mpu6050.gz
    ax = mpu6050.ax
    ay = mpu6050.ay
    az = mpu6050.az
    data = [gx,gy,gz,temp,press,alt,lat,lon]
    time.sleep(1)    
    #open the csv
    with open('Telemetry.csv','a') as csvfile:
        csvfile.write(f"{data}\n")
print("done")

