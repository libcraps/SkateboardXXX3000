import serial
import csv

arduino = serial.Serial('COM9', baudrate=115200, timeout=1.)
line_byte = ''
line_str = ''
datafile = []
isReading = False
ExtractionCompleted = False

compteur= 0

while ExtractionCompleted != True :
    line_byte = arduino.readline()
    line_str = line_byte.decode("utf-8")

    if (line_str != '' and ExtractionCompleted != True):
        isReading = True
        datafile.append(line_str[:-1])
        print("Add Data")

    if (line_str == '' and isReading == True):
        isReading = False
        ExtractionCompleted = True
        print("End of data sheet")

with open("data_session.csv", "w") as file:
    file.writelines(datafile)
