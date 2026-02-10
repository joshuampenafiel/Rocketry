import serial

# Open serial port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    timeout=1
)



line = ser.readline().decode('ascii', errors='replace').strip()
