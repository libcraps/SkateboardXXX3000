import serial

arduino = serial.Serial('COM9', baudrate=115200, timeout=0.01)
arduino.readline()
while (True):
    print(arduino.readline())