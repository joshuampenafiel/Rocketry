import os
import smbus
import board
import busio
import adafruit_bmp3xx
import serial
#setup Stuff
bus = smbus.SMBus(1)
MPU6050_ADDR = 0x68
BMP390_ADDR = 0x42
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43


# Initialize I2C bus



# Wake up MPU-6050 (it starts in sleep mode)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
# ~ print("Imu setup done")

def main():
	ser = serial.Serial(
	port='/dev/ttyS0',
	baudrate=115200,
	timeout=1
	)
	print("gps setup done")


	# Create I2C bus
	#i2c = busio.I2C(board.SCL, board.SDA)


	# Create BMP390 sensor object
	#bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
	bus.write_byte_data(BMP390_ADDR, PWR_MGMT_1, 0)
	print("barrometer setup done")


	exec(open(os.path.join(os.path.expanduser('~'),"Work","Josh","Rocketry","Telemetry.py")).read())
	print("done control")
if __name__ == '__main__':
	main()
