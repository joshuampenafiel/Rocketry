import os
import piexif
import shutil
import linecache
from PIL import Image
import exiftool
from fractions import Fraction
import json


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

def add_coords(image_path,gz,gx,gy, lat, lon, altitude = 0):

    # --- Orientation ---

    "exiftool",
    f"-XMP:Yaw={gz}",
    f"-XMP:Pitch={gy}",
    f"-XMP:Roll={gx}",
    "-overwrite_original",          #prevents a copy from being made

    img = Image.open(image_path)                      
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

    img.save(image_path, exif=exif_bytes)

#------- Custom Tags --------

# ------ Paths-----

Input_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Input")            # Change on Jetson
Output_path = os.path.join(os.path.expanduser('~'),"Projects","Rocketry","File_Move","Output")


#  -----Main Loop-----

if os.path.exists(Input_path):

    for f in os.listdir(Input_path):
        file_path_Input = os.path.join(Input_path,f)
        file_path_Output = os.path.join(Output_path,f)

        if os.path.isfile(file_path_Input):
            #Check CSV for the data
            digits = "".join(ch for ch in f if ch.isdigit())
            i = int(digits)
            data = linecache.getline("Telemetry.csv",i)
            data = data.strip("[]\n")
            gx,gy,gz,temp,press,alt,lat,lon = map(float, data.split(","))

            # Call helper function to add GPS data
            add_coords(file_path_Input,gx,gy,gz, lat, lon, alt)

            # Move file after metadata is added
            shutil.move(file_path_Input, file_path_Output)

            print(f"Processed {f}: ({lat}, {lon}, {alt},{gz})")


else:
    print("Path not found:", Input_path)

print("Done")
