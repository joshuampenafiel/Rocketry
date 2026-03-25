import os
import piexif
import shutil
from PIL import Image
import json
from fractions import Fraction



#-----Helper Functions -----
def dec_to_dms(dec):                                      
    dec = abs(dec)                                          
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

def add_coords(img_path,gz,gx,gy, lat, lon, altitude = 0):

    # --- Orientation ---

    "exiftool",
    f"-XMP:Yaw={gz}",
    f"-XMP:Pitch={gy}",
    f"-XMP:Roll={gx}",
    "-overwrite_original",          #prevents a copy from being made

    img = Image.open(img_path)                      
    exif_dict = piexif.load(img.info.get("exif", piexif.dump({})))  
    lat_ref = "N" if lat >= 0 else "S"                    
    lon_ref = "E" if lon >= 0 else "W"                
    gps_ifd = {                                         
        piexif.GPSIFD.GPSLatitudeRef: lat_ref,              
        piexif.GPSIFD.GPSLongitudeRef: lon_ref,             
        piexif.GPSIFD.GPSAltitudeRef: 0,
        piexif.GPSIFD.GPSLatitude: dms_to_rational(dec_to_dms(lat)),
        piexif.GPSIFD.GPSLongitude: dms_to_rational(dec_to_dms(lon)),
        piexif.GPSIFD.GPSAltitude: (int(altitude * 100), 100),   
    }
        
    exif_dict["GPS"] = gps_ifd            
    exif_bytes = piexif.dump(exif_dict)

    img.save(img_path, exif=exif_bytes)

#------- Custom Tags --------


Input_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Input")            # Change on Jetson
Output_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Output")


#  -----Main Loop-----
brace_count = 0
img_number = 0
buffer = ""
if os.path.exists(Input_path):
#checks if the path exists
    for f in os.listdir(Input_path):
        #checks the amout of images in the folder
        file_path_Input = os.path.join(Input_path,f)
        #joins a file into the Input_path
        file_path_Output = os.path.join(Output_path,f)
        #joins the file to the output path
        with open("telemetry2.json") as f:
            #open the Telemetry2 json as f
            for line in f:
                #checks the amount of lines in the json
                line = line.strip()
                #strips each line
                if not line:
                    continue
                
                # Count braces
                brace_count += line.count("{")
                brace_count -= line.count("}")

                buffer += line

                # When braces balance → full JSON object
                for f in os.listdir(Input_path):
                    #for every file in input
                    img_path= os.path.join(Input_path, f)
                    #join every path together

                    #padds the zeros
                if brace_count == 0 and buffer:
                    if img_number > 9999:
                        file_path_Input = f"frame_{img_number}.jpg"
                    elif img_number > 999:
                        file_path_Input = f"frame_0{img_number}.jpg"    
                    elif img_number > 99:
                        file_path_Input = f"frame_00{img_number}.jpg"   
                    elif img_number > 9:
                        file_path_Input = f"frame_000{img_number}.jpg"   
                    else:
                        file_path_Input = f"frame_0000{img_number}.jpg"


                    #read data
                    entry = json.loads(buffer)
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

        # Call helper function to add GPS data
        add_coords(img_path,gx,gy,gz,alt, lat, lon)

        # Move file after metadata is added
        shutil.move(img_path, Output_path)

        print(f"Processed {f}: ({clock},{temp},{press},{alt},{ax},{ay},{az},{gx},{gy}, {gz}, {lat}, {lon},{fix},{cpu_use_percent},{cpu_temp_c},{cpu_freq_mhz},{mem_use_percent})")


else:
    print("Path not found:", Input_path)

print("Done")
