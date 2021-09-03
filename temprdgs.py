import serial
import time


portname = '/dev/ttyACM0'
ser = serial.Serial(portname, 9600)
time.sleep(2)

while(True):
	line = ser.readline() # read a byte
	decoded_bytes = line[0:len(line)-2].decode()
	print(decoded_bytes)
	time.sleep(0.5)

ser.close()
