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

