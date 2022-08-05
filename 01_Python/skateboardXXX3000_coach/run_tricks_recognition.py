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

############   SETTINGS   #############

print("run_tricks_recognition")
completeSequencesPath = "../../06_Data/sequences/sesh_151121/raw/record_7_interpolated.csv"
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

tricks_with_name=[]
for y in Y_pred:
    tricks_with_name.append(label[y])

df.plot_tricks_recognition_result(complete_sequence, events_interval, label, Y_pred,save=True, path="./report/figures/result_glob.png")

report={}
report["filename"]=complete_sequence.filepath
report["nb_tricks"]=len(Y_pred)
report["tricks"]=tricks_with_name

report["detail"] = get_tricks_features(complete_sequence, events_interval, tricks_with_name)

data_report = {"data":report}

tex = make_report_html(data_report)
print(report["filename"])
with open("./report/sesh_report/result.html","w") as f:
    f.write(tex)

html_path="./report/sesh_report/result.html"
pdf_path = "./report/sesh_report/result.pdf"
html2pdf(html_path, pdf_path)



