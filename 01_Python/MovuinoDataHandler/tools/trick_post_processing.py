import numpy as np
from tools.quaternion import Quaternion

def get_azimuth(trick):
    quaternion=Quaternion()
    theta_list=[]
    for i in range(trick.nb_row):
        quaternion.rotate(trick.gyroscope[:,i]*np.pi/180,trick.Te)
        rot =quaternion.get_rot_mat()
        # theta = np.arctan2(rot.T[1,0],rot.T[1,1])*180/np.pi
        theta = np.abs(np.arctan2(rot.T[1,0],rot.T[1,1])*180/np.pi)
        theta_list.append(theta)
    return theta_list

def get_height(trick):
    return