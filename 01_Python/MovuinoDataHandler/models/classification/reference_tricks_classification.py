
from multiprocessing.dummy import Value
import numpy as np
import pandas as pd
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
from models.classification.classification_template_class import ClassificationTricks
import movuinos.SkateboardXXX3000DataSet as sk
from tools.sk_array_manipulation import array_gyr_normalize
import tools.signal_analysis as sa
import tools.correction_interpolation as ci
import tools.display_functions as disp

class ReferenceTricksClassification(ClassificationTricks):
    def __init__(self, reference_tricks_path, seuil_dist):
        self.ref_360flip = sk.SkateboardXXX3000DataSet(reference_tricks_path + "360_flip_reference.csv")
        self.ref_ollie = sk.SkateboardXXX3000DataSet(reference_tricks_path + "ollie_reference.csv")
        self.ref_kickflip = sk.SkateboardXXX3000DataSet(reference_tricks_path + "kickflip_reference.csv")
        self.ref_heelflip = sk.SkateboardXXX3000DataSet(reference_tricks_path + "heelflip_reference.csv")
        self.ref_pop_shovit = sk.SkateboardXXX3000DataSet(reference_tricks_path + "pop_shovit_reference.csv")
        self.ref_fs_shovit = sk.SkateboardXXX3000DataSet(reference_tricks_path + "fs_shovit_reference.csv")

        self.seuil_dist = seuil_dist
        self.Y_pred = []
        self.label = ['360_flip', 'fs_shovit', 'heelflip', 'kickflip', 'ollie', 'pop_shovit', 'Not tricks']

    def classify(self, events_interval, complete_sequence):
        gyrNormalize_360Flip = array_gyr_normalize(self.ref_360flip.rawData)
        gyrNormalize_ollie = array_gyr_normalize(self.ref_ollie.rawData)
        gyrNormalize_kickflip = array_gyr_normalize(self.ref_kickflip.rawData)
        gyrNormalize_heelflip = array_gyr_normalize(self.ref_heelflip.rawData)
        gyrNormalize_pop_shovit = array_gyr_normalize(self.ref_pop_shovit.rawData)
        gyrNormalize_fs_shovit = array_gyr_normalize(self.ref_fs_shovit.rawData)

        for i, interval in enumerate(events_interval):
            tricks = complete_sequence.rawData.loc[interval[0]:interval[1], :]

            newDF = ci.correction_interpolation(tricks)
            newDF = sk.SkateboardXXX3000DataSet.normalized_L2(newDF.copy())
            try :
                # distance euclidienne
                tricksGyr_normalized = array_gyr_normalize(newDF.copy())
                # tricksGyr_normalized = tricksGyr_normalized/np.linalg.norm(tricksGyr_normalized)
                # gyrNormalize_ollie = gyrNormalize_ollie/np.linalg.norm(gyrNormalize_ollie)
                # gyrNormalize_kickflip = gyrNormalize_kickflip/np.linalg.norm(gyrNormalize_kickflip)
                # gyrNormalize_heelflip = gyrNormalize_heelflip/np.linalg.norm(gyrNormalize_heelflip)
                # gyrNormalize_pop_shovit = gyrNormalize_pop_shovit/np.linalg.norm(gyrNormalize_pop_shovit)
                # gyrNormalize_fs_shovit = gyrNormalize_fs_shovit/np.linalg.norm(gyrNormalize_fs_shovit)
                # gyrNormalize_360Flip = gyrNormalize_360Flip/np.linalg.norm(gyrNormalize_360Flip)

                dist_euc_file = np.zeros(shape=(6, 1))
                dist_euc_file[4] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_ollie, axis=0))
                dist_euc_file[3] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_kickflip, axis=0))
                dist_euc_file[2] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_heelflip, axis=0))
                dist_euc_file[5] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_pop_shovit, axis=0))
                dist_euc_file[1] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_fs_shovit, axis=0))
                dist_euc_file[0] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_360Flip, axis=0))

                minVal = np.amin(dist_euc_file)
                ind = np.argmin(dist_euc_file)
                print(minVal)
                print(ind)
                # tricks pas tricks ?
                if minVal > self.seuil_dist:
                    self.Y_pred.append(len(self.label) - 1)
                else:
                    self.Y_pred.append(ind)
            except ValueError:
                self.Y_pred.append(404)
        return self.Y_pred


