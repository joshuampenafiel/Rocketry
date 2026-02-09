import time
import board
import busio
import adafruit_bmp3xx

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create BMP390 sensor object
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# Optional configuration
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2
bmp.sea_level_pressure = 1013.25  # hPa (adjust for your location)

print("Reading BMP390 data... Press Ctrl+C to stop")

try:
    while True:
        temperature = bmp.temperature
        pressure = bmp.pressure
        altitude = bmp.altitude

        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure:    {pressure:.2f} hPa")
        print(f"Altitude:    {altitude:.2f} m")
        print("-" * 40)
        

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped.")
