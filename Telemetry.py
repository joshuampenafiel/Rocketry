import csv
import bmp390
import gps
import mpu6050
#record data
while True:
    line = gps.line
    if line.startswith('$GNRMC'):
        parts = line.split(",")
        lat = parts[3] 
        lon = parts[5]              
    temp = bmp390.temperature
    press = bmp390.pressure
    alt = bmp390.altitude
    gx = gps.gx
    gy = gps.gy
    gz = gps.gz
    ax = gps.ax
    ay = gps.ay
    az = gps.az
    data = [gx,gy,gz,temp,press,alt,lat,lon]    
    #open the csv
    with open('Telemetry.csv','a') as csvfile:
        csvfile.write(f"{data}\n")
print("done")

