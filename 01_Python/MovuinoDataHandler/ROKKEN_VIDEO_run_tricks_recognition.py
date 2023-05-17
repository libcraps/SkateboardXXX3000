import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

import os
import jinja2
import pdfkit
import pandas as pd
import numpy as np
from datetime import date
# Marche pas avec mon environnement conda
from pdflatex import PDFLaTeX

import movuinos.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.signal_analysis as sa
import tools.correction_interpolation as ci

from tools.get_tricks_features import get_tricks_features

import models.detection.detection_energy as dt
import models.classification.reference_tricks_classification as rtc

from report.tools.make_report_latex import make_report_latex
from report.tools.make_report_html import make_report_html
from report.tools.html2pdf import html2pdf
import numpy as np
import matplotlib.pyplot as plt
import cv2
from os import listdir, mkdir
from pathlib import Path
import copy
############   SETTINGS   #############

print("run_tricks_recognition")
completeSequencesPath = "../../06_Data/sequences/sesh_160122/raw/record_1_interpolated.csv"
reference_tricks_path = "../../06_Data/Reference_tricks/"

#--- Opening file ---
print("Opening : " + completeSequencesPath)
complete_sequence = sk.SkateboardXXX3000DataSet(completeSequencesPath)
Te = complete_sequence.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

prominence = 5 #3
distance = 4 #4

#seuil distance pour la classification
seuil = 0.045 #0.0121

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
# video = cv2.VideoWriter('ct_segmentation.mp4', fourcc, 1, (1200, 600))
video = cv2.VideoWriter('skateboard.mp4', fourcc, 10, (2000, 1000))


detection_model = dt.DetectionEnergy()
events_interval = detection_model.detect(complete_sequence, size_window, overlap, prominence, distance)

classification_model = rtc.ReferenceTricksClassification(reference_tricks_path, seuil)
Y_pred = classification_model.classify(events_interval, complete_sequence)
label = classification_model.label
#raté pas raté ?

tricks_with_name=[]
for y in Y_pred:
    tricks_with_name.append(label[y])
# df.plot_tricks_recognition_result(complete_sequence, events_interval, label, Y_pred,save=True, path="./report/figures/result_glob.png")

from tqdm import tqdm

# print(time_list)
# print(len(time_list))

win_obs = 1000
dec=100


file=pd.read_csv("../../06_Data/sequences/sesh_160122/raw/record_1_interpolated.csv")
zeros=[0]*dec
dict_ = dict()
for i in file.columns:
    dict_[i]=zeros

df_zeros=pd.DataFrame(dict_)
for i in tqdm(range(76)):
    print("((((((((((((((((((   ", i)

    s=i*dec
    e=s+win_obs
    
    # frames = [df_zeros, file.iloc[s:e], df_zeros]
    frames=file.iloc[s:e]
    # result = pd.concat(frames)
    result = frames
    result.to_csv("temp.csv")
    complete_sequence = sk.SkateboardXXX3000DataSet("temp.csv")
    detection_model = dt.DetectionEnergy()
    events_interval = detection_model.detect(complete_sequence, size_window, overlap, prominence, distance)
    # events_interval =[[0,119]]
    classification_model = rtc.ReferenceTricksClassification(reference_tricks_path, seuil)
    Y_pred = classification_model.classify(events_interval, complete_sequence)
    label = classification_model.label
    #raté pas raté ?

    tricks_with_name=[]
    for y in Y_pred:
        if y != 404:
            tricks_with_name.append(label[y])
        else : 
            tricks_with_name.append("error")

    # df.plot_tricks_recognition_result(complete_sequence, events_interval, label, Y_pred,save=True, path="./report/figures/result_glob.png")

    time_list = np.array(complete_sequence.time)
    
    fig = plt.figure(figsize=(20,10))
    df.plotVect(time_list, complete_sequence.acceleration, 'Acceleration (m/s2)', 231)
    plt.ylim([-100,150])
    plt.xlabel("Temps (s)")
    plt.legend(loc='upper right')
    plt.grid()
    df.plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 232)
    plt.ylim([-650,650])
    plt.xlabel("Temps (s)")
    plt.legend(loc='upper right')
    plt.grid()
    plt.subplot(233)
    plt.imshow(np.zeros(shape=(50,50)))
    plt.subplot(234)
    plt.plot(time_list, complete_sequence.normAcceleration, label='Norme Accélération', color="black")
    plt.plot(detection_model.time_win,detection_model.sum_acc,'-o', markersize=2)
    if events_interval!=[]:
        
        plt.plot(detection_model.time_win[detection_model.peaks_a], detection_model.sum_acc[detection_model.peaks_a], "v", markersize=5, color="orange", label="Peaks")
        plt.plot(detection_model.time_win[detection_model.peaks_tricks], detection_model.sum_acc[detection_model.peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
    plt.grid()
    plt.ylim([-10,130])
    plt.legend(loc='upper right')

    plt.subplot(235)
    plt.plot(time_list, complete_sequence.normGyroscope, label="Norme gyroscope", color="black")
    plt.plot(detection_model.time_win, detection_model.sum_gyr,'-o', markersize=2)
    if events_interval!=[]:
        
        plt.plot(detection_model.time_win[detection_model.peaks_gyr], detection_model.sum_gyr[detection_model.peaks_gyr], "v", markersize=5, color="orange", label="Peaks")
        plt.plot(detection_model.time_win[detection_model.peaks_tricks], detection_model.sum_gyr[detection_model.peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
    plt.grid()
    plt.ylim([-10,850])
    df.plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 236)
    for i, interval in enumerate(events_interval):
        i_start = interval[0]
        i_end = interval[1]
        plt.plot(
            [complete_sequence.time[i_start], complete_sequence.time[i_start], complete_sequence.time[i_end],
                complete_sequence.time[i_end],
                complete_sequence.time[i_start]], [-abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                -abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                -abs(max(complete_sequence.normGyroscope[i_start:i_end]))], color="r")
        plt.text(complete_sequence.time[i_start], max(complete_sequence.normGyroscope[i_start:i_end]) + 50,
                    "{}".format(tricks_with_name[i], fontsize=20))
    plt.legend(loc='upper right')
    plt.xlabel("Temps (s)")
    plt.grid()
    # plt.ylim([-max(complete_sequence.normGyroscope) * 1.2, max(complete_sequence.normGyroscope) * 1.2])
    plt.ylim([-700,700])
    
    fig.canvas.draw()
    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    image_from_plot = cv2.cvtColor(image_from_plot, cv2.COLOR_RGB2BGR)

    if i == 0:
        print("image_from_plot", image_from_plot.shape)

    video.write(image_from_plot)
    plt.savefig("tmp.png")
    plt.close(fig)
    del complete_sequence
video.release()