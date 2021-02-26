import serial

arduino = serial.Serial('COM9', baudrate=115200, timeout=1.)
while (True):
    line = arduino.readline()
    print(line[:-2])