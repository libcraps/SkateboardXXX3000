import dataSet.SkateboardXXX3000DataSet as sk
import os
import numpy as np
import random
from sklearn.svm import SVC
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"
#folderPath = "..\\..\\06 - Data\\Raw_sequences\\"

labelNamesAll = []

for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    labelNamesAll.append(sousRepertoires)
    for file in fichiers:
        if "interpolated" in file:
            print(file)
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            print(skateDataSet.nb_row)

print(labelNamesAll[0])
labelNamesAll = labelNamesAll[0]
#build DATASET from K categories and (up to) N images from category
K = 3
N = 1000

#selection of label indices
X = np.zeros([K*N,100*100]) #data matrix, one image per row
#Y = np.zeros([K*N,1]) #label indices
Y = -np.ones([K*N,1]) #label indices
labelNames = []

random.seed(a=42) #uncomment to make errors reproducible/comment to see variability

globalCount = 0
for i in range(K):
    while True:
        lab = random.randint(0,len(labelNamesAll)-1)
        if lab not in labelNames:
            break
    #folders are named after the class label
    filedir = os.path.join(folderPath,labelNamesAll[lab])
    print(filedir)

    #save the name of the class
    labelNames.append(labelNamesAll[lab])

    classCount = 0
    for filename in os.listdir(filedir):
        f = os.path.join(filedir, filename)
        if f.endswith(('.csv')) and (classCount < N):
            tricks = sk.SkateboardXXX3000DataSet(f)
            print(tricks.rawData.shape)
            X[globalCount,:] = tricks.rawData
            Y[globalCount,:] = i
            globalCount += 1
            classCount += 1

#Remove the unused entries of X and Y
print("Total number of samples",globalCount)
X = X[:globalCount,:]
Y = Y[:globalCount,:]

#Check the stored classes
print("used labels",labelNames)
print("Size of data matrix", X.shape)
print("clas labels", Y.T)