
import numpy as np
import pandas as pd
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
from models.detection.detection_template_class import DetectionTricks

import tools.signal_analysis as sa

class DetectionEnergy(DetectionTricks):
    def __init_(self):
        DetectionTricks.__init__.super()
        self.time_win = [] 
        self.tricks_interval_temp = []
        self.peaks_gyr = []
        self.peaks_a = []
        self.peaks_tricks = []

        self.events_interval = [[]]
    
    def event_detection(self, skate_dataset, size_window,overlap, prominence, distance):
        if size_window % 2 == 0:
            size_window += 1

        window = [0, size_window]
        retard = size_window // 2

        sum_acc = []
        sum_gyr = []

        time_win = []

        output = []

        normAcc = np.pad(skate_dataset.normAcceleration, (int(size_window // 2), int(size_window // 2)))
        normGyr = np.pad(skate_dataset.normGyroscope, (int(size_window // 2), int(size_window // 2)))

        while window[1] < len(skate_dataset.time):
            time_win.append(skate_dataset.time[(window[0] + window[1]) // 2 - retard])
            sum_acc.append(np.mean(normAcc[window[0]:window[1]]))
            sum_gyr.append(np.mean(normGyr[window[0]:window[1]]))

            window[0] += size_window - overlap
            window[1] += size_window - overlap

        sum_gyr = np.array(sum_gyr)
        sum_acc = np.array(sum_acc)
        peaks_gyr, _gyr = find_peaks(sum_gyr, prominence=prominence, distance=distance)
        peaks_acc, _acc = find_peaks(sum_acc, prominence=prominence - 1, distance=distance - 2)
        time_win = np.array(time_win)

        peaks_tricks = []
        delta_peak = 2

        for i, peak_a in enumerate(peaks_acc):
            for j, peak_g in enumerate(peaks_gyr):
                if peak_g - delta_peak < peak_a < peak_g + delta_peak:
                    peaks_tricks.append(peak_g)

        dt_i = 0.8


        tricks_interval = []
        for i in peaks_tricks:
            if time_win[i] - dt_i < 0:
                tricks_interval.append([0.1, time_win[i] + dt_i])
            else:
                tricks_interval.append([time_win[i] - dt_i, time_win[i] + dt_i])
        #return super().detect()
        return time_win, tricks_interval, peaks_gyr, peak_a, peaks_tricks
        
    def center_events(self,skate_dataset,tricks_interval, dt_f = 0.6):
        time_list = []
        Te = skate_dataset.Te
        for k in range(len(tricks_interval)):
            # We're looking for the best index that matches with the time interval
            i_start = int(float(tricks_interval[k][0] - 0.1) / Te)
            i_end = int(float(tricks_interval[k][1] - 0.1) / Te)

            while skate_dataset.time[i_start] < tricks_interval[k][0]:
                i_start += 1

            while skate_dataset.time[i_end] < tricks_interval[k][1]:
                i_end += 1

            df_iso_tricks = skate_dataset.interpolateData.iloc[i_start:i_end, :]

            normGyroscope = list(df_iso_tricks["normGyr"])
            time = list(df_iso_tricks["time"])

            # ---- Temps moyen de la norme du gyrosocpe ------
            index_mean_loc = sa.mean_time(normGyroscope)

            # teeest :
            # g = np.cumsum(skateDataSet.normGyroscope[i_start:i_end])
            # index_mean_loc = np.argmin(np.abs(g - np.amax(g) / 2))
            mean_time = skate_dataset.time[i_start] + index_mean_loc * Te

            new_tricks_interval = [mean_time - dt_f, mean_time + dt_f]
            i_start = 0
            i_end = 0
            while skate_dataset.time[i_start] < new_tricks_interval[0]:
                i_start += 1

            while skate_dataset.time[i_end] < new_tricks_interval[1]:
                i_end += 1

            time_list.append([i_start,i_end])
        return time_list

    def detect(self,data, size_window,overlap,prominence,distance):
        self.time_win, self.tricks_interval_temp, self.peaks_gyr, self.peaks_a, self.peaks_tricks = self.event_detection(data, size_window,overlap,prominence,distance)
        self.events_interval = self.center_events(data,  self.tricks_interval_temp)

        return self.events_interval
        

        
    