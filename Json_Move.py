import os
import piexif
import shutil
from PIL import Image
import json
from fractions import Fraction
import sys

# ----- Helper Functions -----

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

def float_to_rational(value):
    f = Fraction(str(value)).limit_denominator()
    return (f.numerator, f.denominator)

def encode_usercomment(comment_str):
    return b"ASCII\x00\x00\x00" + comment_str.encode("utf-8")


# ----- Velocity Integration -----

class VelocityIntegrator:
    """Integrates acceleration over time using the trapezoidal rule."""
    def __init__(self):
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.prev_ts  = None
        self.prev_ax  = 0.0
        self.prev_ay  = 0.0
        self.prev_az  = 0.0

    def update(self, timestamp, ax, ay, az):
        if self.prev_ts is not None:
            dt = timestamp - self.prev_ts
            if dt > 0:
                self.vx += (self.prev_ax + ax) / 2.0 * dt
                self.vy += (self.prev_ay + ay) / 2.0 * dt
                self.vz += (self.prev_az + az) / 2.0 * dt

        self.prev_ts = timestamp
        self.prev_ax = ax
        self.prev_ay = ay
        self.prev_az = az

        return self.vx, self.vy, self.vz


# ----- Core Write Function -----

def add_coords(img_path, lat, lon, altitude,
               clock, temp, press,
               ax, ay, az,
               gx, gy, gz,
               vx, vy, vz,
               cpu_use_percent, cpu_temp_c, cpu_freq_mhz, mem_use_percent):

    print(f"  Opening: {img_path}")
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        print(f"  ERROR: File not found — {img_path}")
        return False

    exif_dict = piexif.load(img.info.get("exif", piexif.dump({})))

    # --- GPS IFD ---
    # Guard against null GPS (no fix yet)
    if lat is not None and lon is not None:
        lat_ref = "N" if lat >= 0 else "S"
        lon_ref = "E" if lon >= 0 else "W"
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef:  lat_ref.encode(),
            piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode(),
            piexif.GPSIFD.GPSAltitudeRef:  0,
            piexif.GPSIFD.GPSLatitude:     dms_to_rational(dec_to_dms(lat)),
            piexif.GPSIFD.GPSLongitude:    dms_to_rational(dec_to_dms(lon)),
            piexif.GPSIFD.GPSAltitude:     (int(altitude * 100), 100),
        }
        exif_dict["GPS"] = gps_ifd
    else:
        print("  WARNING: No GPS fix — skipping GPS EXIF fields")

    # --- Custom Sensor Data in UserComment ---
    custom_data = {
        # Accelerometer (m/s^2)
        "ax": ax, "ay": ay, "az": az,
        # Gyroscope (deg/s)
        "gx": gx, "gy": gy, "gz": gz,
        # Integrated Velocity (m/s)
        "vx": round(vx, 6),
        "vy": round(vy, 6),
        "vz": round(vz, 6),
        # Barometric
        "alt_baro": altitude,
        "temp_c":   temp,
        "press_hpa": press,
        # Timestamp
        "ts": clock,
        # System
        "cpu_%":  cpu_use_percent,
        "cpu_t":  cpu_temp_c,
        "cpu_mhz": cpu_freq_mhz,
        "mem_%":  mem_use_percent,
    }

    exif_dict["Exif"][piexif.ExifIFD.UserComment] = encode_usercomment(json.dumps(custom_data))
    exif_dict.pop("thumbnail", None)

    exif_bytes = piexif.dump(exif_dict)
    img.save(img_path, exif=exif_bytes)
    print(f"  Saved:  {img_path}")
    return True


# ----- JSON Parsing -----

def read_data(minijson):
    entry = json.loads(minijson)

    clock = entry["timestamp"]
    bmp   = entry["sensors"]["bmp390"]
    mpu   = entry["sensors"]["mpu6050"]
    gps   = entry["gps"]
    sys_  = entry["system"]

    return {
        "clock":    clock,
        "temp":     bmp["temperature"],
        "press":    bmp["pressure"],
        "alt":      bmp["altitude"],
        "ax":       mpu["accel"]["x"],
        "ay":       mpu["accel"]["y"],
        "az":       mpu["accel"]["z"],
        "gx":       mpu["gyro"]["x"],
        "gy":       mpu["gyro"]["y"],
        "gz":       mpu["gyro"]["z"],
        "lat":      gps["lat"],
        "lon":      gps["lon"],
        "fix":      gps["fix"],
        "cpu_%":    sys_["cpu_usage_percent"],
        "cpu_t":    sys_["cpu_temp_c"],
        "cpu_mhz":  sys_["cpu_freq_mhz"],
        "mem_%":    sys_["memory_usage_percent"],
    }


# ----- Paths -----

Input_path = os.path.join(os.path.expanduser("~"), "Projects", "Rocketry", "File_Move", "Input")
Output_path = os.path.join(os.path.expanduser("~"), "Projects", "Rocketry", "File_Move", "Output")
json_path   = os.path.join(os.path.expanduser("~"), "Projects", "Rocketry", "File_Move", "File_Move_Code", "telemetry2.json")

# ----- Main -----

if not os.path.exists(Input_path):
    print(f"ERROR: Input path does not exist — {Input_path}")
    sys.exit(1)

integrator  = VelocityIntegrator()
img_number  = 0
brace_count = 0
minijson    = ""

print(f"Processing images from: {Input_path}")

with open(json_path) as tel:
    for line in tel:
        brace_count += line.count("{")
        brace_count -= line.count("}")
        minijson    += line

        if brace_count == 0 and minijson.strip():
            img  = f"frame_{img_number:05d}.jpg"
            src  = os.path.join(Input_path,  img)
            dst  = os.path.join(Output_path, img)

            if not os.path.exists(src):
                print(f"WARNING: {img} not found in Input, skipping JSON entry")
                minijson = ""
                img_number += 1
                continue

            print(f"\n[{img_number}] {img}")

            try:
                d = read_data(minijson)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  ERROR parsing JSON entry {img_number}: {e}")
                minijson = ""
                img_number += 1
                continue

            # Calculate velocity from acceleration
            vx, vy, vz = integrator.update(d["clock"], d["ax"], d["ay"], d["az"])

            success = add_coords(
                img_path         = src,
                lat              = d["lat"],
                lon              = d["lon"],
                altitude         = d["alt"],
                clock            = d["clock"],
                temp             = d["temp"],
                press            = d["press"],
                ax               = d["ax"],
                ay               = d["ay"],
                az               = d["az"],
                gx               = d["gx"],
                gy               = d["gy"],
                gz               = d["gz"],
                vx               = vx,
                vy               = vy,
                vz               = vz,
                cpu_use_percent  = d["cpu_%"],
                cpu_temp_c       = d["cpu_t"],
                cpu_freq_mhz     = d["cpu_mhz"],
                mem_use_percent  = d["mem_%"],
            )

            if success:
                shutil.move(src, dst)
                print(f"  Moved  → {dst}")

            minijson = ""
            img_number += 1

print(f"\nDone — {img_number} images processed.")