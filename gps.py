import serial

# Open serial port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    timeout=1
)

print("Listening for GNRMC sentences...")

try:
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()
        # Check for GNRMC sentence
        if line.startswith('$GNRMC'):
            print(line)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
