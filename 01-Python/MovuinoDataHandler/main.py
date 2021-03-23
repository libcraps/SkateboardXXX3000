import serial
import csv
import matplotlib.pyplot as plt
import pandas as pd
from integratinoFunctions import *
from DisplayFunctions import Display
from mvtAnalyseFunctions import OnGround
import os


folderPath = "..\\_data\\"
fileName = "test_mov_lateral"
fullDataPath = folderPath + fileName

isReading = False
ExtractionCompleted = False
dataManage = True

arduino = serial.Serial('COM9', baudrate=115200, timeout=1.)
line_byte = ''
line_str = ''
datafile = []

# --------- Data Extraction from Movuino ----------
while ExtractionCompleted != True :
    line_byte = arduino.readline()
    line_str = line_byte.decode("utf-8")



    if ("XXX_end" in line_str and isReading == True):
        isReading = False
        ExtractionCompleted = True
        print("End of data sheet")

    if (isReading):
        datafile.append(line_str[:-1])
        print("Add Data")

    if ("XXX_beginning" in line_str):
        isReading = True




with open(fullDataPath + ".csv", "w") as file:
    file.writelines(datafile)

#Data MAnage
if ExtractionCompleted and dataManage:

    rawData = pd.read_csv(fullDataPath + ".csv", sep=",")

    print(rawData.columns)
    time = []
    acceleration = [[], [], []]
    gyroscope = [[], [], []]
    magnetometer = [[], [], []]

    normAcceleration = []
    normGyroscope = []
    normMagnetometer = []

    velocity = [[0], [0], [0]]
    pos = [[0], [0], [0]]
    posAng = [[0], [0], [0]]

    print(rawData)
    rawData["time"] = [k for k in range(len(rawData["ax"]))]
    time = list(rawData["time"])

    acceleration[0] = list(rawData["ax"])  # accelX
    acceleration[1] = list(rawData["ay"])  # accelY
    acceleration[2] = list(rawData["az"])  # accelZ
    gyroscope[0] = list(rawData["gx"])  # gyroX
    gyroscope[1] = list(rawData["gy"])  # gyroY
    gyroscope[2] = list(rawData["gz"])  # gyroZ
    magnetometer[0] = list(rawData["mx"])  # magX
    magnetometer[1] = list(rawData["my"])  # magY
    magnetometer[2] = list(rawData["mz"])  # magZ

    """
    for i in range(3):
        velocity[i] = Euler(time, acceleration[i], velocity[i][0])
        pos[i] = Euler(time, velocity[i], pos[i][0])
        posAng[i] = Euler(time, gyroscope[i], posAng[i][0])
        
    """
    normAcceleration = EuclidienNormListVector(acceleration)
    normGyroscope = EuclidienNormListVector(gyroscope)
    normMagnetometer = EuclidienNormListVector(magnetometer)
    """
    Display("a,v,pos", time, acceleration, velocity, pos)
    Display("omega, theta", time, gyroscope, posAng)
    Display("Magnetometer", time, magnetometer)
    """
    Display("a", time, acceleration)
    """
    rawData["posAngX"] = posAng[0]
    rawData["posAngY"] = posAng[1]
    rawData["posAngZ"] = posAng[2]
    rawData["VelocityX"] = velocity[0]
    rawData["VelocityY"] = velocity[1]
    rawData["VelocityZ"] = velocity[2]
    rawData["posX"] = pos[0]
    rawData["posY"] = pos[1]
    rawData["posZ"] = pos[2]
    """

    rawData["normAccel"] = normAcceleration
    rawData["normGyr"] = normGyroscope
    plt.figure()
    plt.plot(time, normAcceleration)
    plt.show()


    rawData.to_csv(fullDataPath + "treated" + ".csv", sep=",", index=False, index_label=False)