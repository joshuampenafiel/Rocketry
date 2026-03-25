import os
import piexif
import shutil
from PIL import Image
import json
from fractions import Fraction
import sys


#-----Helper Functions -----
def dec_to_dms(dec):                 
    try:                       
        dec = abs(dec)                                          
    except TypeError:
        dec = 0
    degrees = int(dec)                                   
    minutes_float = (dec - degrees) * 60                    
    minutes = int(minutes_float)                          
    seconds = round((minutes_float - minutes) * 60, 5)      
    return degrees, minutes, seconds

def dms_to_rational(dms):                                 
    deg, min_, sec = dms                               
    return (
        (deg, 1),                                          
        (min_, 1),
        (int(sec * 100), 100)
    )

def float_to_rational(deg):
    f = Fraction(str(deg)).limit_denominator()
    return (f.numerator, f.denominator)

def add_coords(img_path,lat, lon, altitude = 0):

    # --- Orientation ---

    # "exiftool",
    # f"-XMP:Yaw={gz}",
    # f"-XMP:Pitch={gy}",
    # f"-XMP:Roll={gx}",
    # "-overwrite_original",          #prevents a copy from being made 
    print("Opening Image")
    try:
        img = Image.open(img_path)        
    except FileNotFoundError:
        print("File not Found Ending Program")
        sys.exit(1)

        

    print("Image Opened\ncreating Dict")
    exif_dict = piexif.load(img.info.get("exif", piexif.dump({})))  
    print("Creating Ref Points")
    lat_ref = "N" if lat is not None and lat >= 0 else "S"                     
    lon_ref = "E" if lon is not None and lon >= 0 else "W"        
    print("Ref Points completed\nCreating ifd")
    gps_ifd = {                                         
        piexif.GPSIFD.GPSLatitudeRef: lat_ref,              
        piexif.GPSIFD.GPSLongitudeRef: lon_ref,             
        piexif.GPSIFD.GPSAltitudeRef: 0,
        piexif.GPSIFD.GPSLatitude: dms_to_rational(dec_to_dms(lat)),
        piexif.GPSIFD.GPSLongitude: dms_to_rational(dec_to_dms(lon)),
        piexif.GPSIFD.GPSAltitude: (int(altitude * 100), 100),   
    }
    print("ifd created\n setting dict = ifd")
    exif_dict["GPS"] = gps_ifd    
  

    print("dict set = to ifd\n popping thumbnail")
    exif_dict.pop("thumbnail", None)
    print("Thumbnail popped\n adding thex exif_bytes")
    exif_bytes = piexif.dump(exif_dict) 
    print("exifbytes = exif_dict\n saving image")
    img.save(img_path, exif=exif_bytes)
    print("Image saved\n Leaving Function")


def read_data(minijson):
    print("Loading Data")
    entry = json.loads(minijson)
    print("Saving Telemetry")
    clock = entry["timestamp"]

    bmp = entry["sensors"]["bmp390"]
    mpu = entry["sensors"]["mpu6050"]
    gps = entry["gps"]
    sys = entry["system"]

    temp = bmp["temperature"]
    press = bmp["pressure"]
    alt = bmp["altitude"]

    ax = mpu["accel"]["x"]
    ay = mpu["accel"]["y"]
    az = mpu["accel"]["z"]

    gx = mpu["gyro"]["x"]
    gy = mpu["gyro"]["y"]
    gz = mpu["gyro"]["z"]

    lat = gps["lat"]
    lon = gps["lon"]
    fix = gps["fix"]

    cpu_use_percent = sys["cpu_usage_percent"]
    cpu_temp_c = sys["cpu_temp_c"]
    cpu_freq_mhz = sys["cpu_freq_mhz"]
    mem_use_percent = sys["memory_usage_percent"]
    

    return clock,temp,press,alt,ax,ay,az,gx,gy,gz,lat,lon,fix,cpu_use_percent,cpu_temp_c,cpu_freq_mhz,mem_use_percent

#------- Custom Tags --------

# ------ Variables ----------
img_number = 0
brace_count = 0
Input_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Input")            # Change on Jetson
Output_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Output")
json_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","File_Move_Code","telemetry2.json")
minijson = ""
data = ()

#begin by opening the folder

if os.path.exists(Input_path):
    #read next image starting at img 0
    #Open Json
    with open(json_path) as tel:
        for line in tel:
            lines = line.strip()
        for f in os.listdir(Input_path):
            #zero pad img_number to get the right string

            tel.seek(0)
    #add telemetry to image

            #Split Json into each individual Json

            for line in tel:
                img = f"frame_{img_number:05d}.jpg"
                file_path_Input = os.path.join(Input_path,img)
                file_path_Output = os.path.join(Output_path,img)
                brace_count +=line.count("{")
                brace_count -=line.count("}")
                minijson += line
                print (f"Brace count = {brace_count}")
                if brace_count == 0:
                    #Read Json
                    data = read_data(minijson)
                    print("Data has been read")
                    minijson = ""
                    clock, temp, press, alt, ax, ay, az, gx, gy, gz, lat, lon, fix, cpu_use_percent, cpu_temp_c, cpu_freq_mhz, mem_use_percent  = data  
                    #Add Telemetry

                    add_coords(file_path_Input,lat,lon,alt)
                    img_number+=1
                    print (f"image number is {img_number}")
                    shutil.move(file_path_Input, Output_path)
    print("Done reading !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")

    #move img to output
    #loop back to reading image

else:
    print("doesn't exist")

