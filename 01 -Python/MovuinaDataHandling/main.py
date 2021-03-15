import matplotlib.pyplot as plt
import pandas as pd
from integratinoFunctions import Euler, Offset
from DisplayFunctions import Display
from mvtAnalyseFunctions import OnGround
import os

dataPath = "..\\Data\\"
fileName = "DropIn\\data_session"
#fileName = "dataTestTemplate.csv"

rawData = pd.read_csv(dataPath + fileName + ".csv", sep=",")

time = []
acceleration = [[],[],[]]
gyroscope = [[],[],[]]
magnetometer = [[],[],[]]

velocity = [[0],[0],[0]]
pos = [[0],[0],[0]]
posAng = [[0],[0],[0]]

print(rawData)
time = list(rawData["time"])

acceleration[0] = list(rawData["ax"]) #accelX
acceleration[1] = list(rawData["ay"]) #accelY
acceleration[2] = list(rawData["az"]) #accelZ
gyroscope[0] = list(rawData["gx"]) #gyroX
gyroscope[1] = list(rawData["gy"]) #gyroY
gyroscope[2] = list(rawData["gz"]) #gyroZ
magnetometer[0] = list(rawData["mx"]) #magX
magnetometer[1] = list(rawData["my"]) #magY
magnetometer[2] = list(rawData["mz"]) #magZ

#OnGround(time, acceleration[2], [], 5)
print(type(acceleration[2][2]))
#acceleration[2] = Offset(acceleration[2])
"""
for i in range(3):
    velocity[i] = Euler(time, acceleration[i], velocity[i][0])
    pos[i] = Euler(time, velocity[i], pos[i][0])
    posAng[i] = Euler(time, gyroscope[i], posAng[i][0])

Display("a,v,pos", time, acceleration, velocity, pos)
Display("omega, theta", time, gyroscope, posAng)
Display("Magnetometer", time, magnetometer)
"""
Display("a", time, acceleration)


rawData["posAngX"] = posAng[0]
rawData["posAngY"] = posAng[1]
rawData["posAngZ"] = posAng[2]
rawData["VelocityX"] = velocity[0]
rawData["VelocityY"] = velocity[1]
rawData["VelocityZ"] = velocity[2]
rawData["posX"] = pos[0]
rawData["posY"] = pos[1]
rawData["posZ"] = pos[2]

rawData.to_csv(dataPath+fileName+"integrate" + ".csv", sep=",", index=False, index_label=False)
print(rawData)


