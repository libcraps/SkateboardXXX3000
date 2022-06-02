import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

import movuinos.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.signal_analysis as sa
import tools.correction_interpolation as ci

import models.detection.detection_energy as dt
import models.classification.reference_tricks_classification as rtc

############   SETTINGS   #############
completeSequencesPath = "..\\..\\06_Data\\Raw_sequences\\sesh_151121_\\record_7_interpolated.csv"
reference_tricks_path = "..\\..\\06_Data\\Reference_tricks\\"

#--- Opening file ---
print("Opening : " + completeSequencesPath)
complete_sequence = sk.SkateboardXXX3000DataSet(completeSequencesPath)
Te = complete_sequence.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

prominence = 3
distance = 4

#seuil distance pour la classification
seuil = 0.0121

#----------------
#extract every event of the complete path
detection_model = dt.DetectionEnergy()
events_interval = detection_model.detect(complete_sequence, size_window, overlap, prominence, distance)

classification_model = rtc.ReferenceTricksClassification(reference_tricks_path, seuil)
Y_pred = classification_model.classify(events_interval, complete_sequence)
label = classification_model.label

#raté pas raté ?

plt.figure(figsize=(10,20))
time_list = np.array(complete_sequence.time)

df.plotVect(time_list, complete_sequence.acceleration, 'Acceleration (m/s2)', 221)
plt.xlabel("Temps (s)")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(223)
plt.plot(time_list, complete_sequence.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.grid()
df.plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 222)
plt.xlabel("Temps (s)")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(224)
plt.plot(time_list, complete_sequence.normGyroscope, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.grid()
plt.show()
df.plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 211)

for i, interval in enumerate(events_interval):
    i_start = interval[0]
    i_end = interval[1]
    plt.plot(
        [complete_sequence.time[i_start], complete_sequence.time[i_start], complete_sequence.time[i_end], complete_sequence.time[i_end],
         complete_sequence.time[i_start]], [-abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            -abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            -abs(max(complete_sequence.normGyroscope[i_start:i_end]))], color="r")
    plt.text(complete_sequence.time[i_start], max(complete_sequence.normGyroscope[i_start:i_end]) + 50, "{}".format(label[Y_pred[i]], fontsize=20))
plt.legend(loc='upper right')
plt.xlabel("Temps (s)")
plt.grid()
plt.ylim([-max(complete_sequence.normGyroscope) * 1.2, max(complete_sequence.normGyroscope) * 1.2])
plt.subplot(212)
plt.plot(time_list, complete_sequence.normGyroscope, label="Norme gyroscope", color="black")
plt.legend(loc='upper right')
plt.grid()
plt.show()
