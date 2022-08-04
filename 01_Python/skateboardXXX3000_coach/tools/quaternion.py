import numpy as np


class Quaternion:
    def __init__(self):
        self.q = np.array([1, 0, 0, 0])  # Initial state of the quaternion

    def rotate(self, w, dt):
        q = self.q
        Sq = np.array([[-q[1], -q[2], -q[3]],
                       [q[0], -q[3], q[2]],
                       [q[3], q[0], -q[1]],
                       [-q[2], q[1], q[0]]])
        self.q = np.matmul(dt/2 * Sq, np.array(w).transpose()) + q


    def get_rot_mat(self):
        c00 = self.q[0] ** 2 + self.q[1] ** 2 - self.q[2] ** 2 - self.q[3] ** 2
        c01 = 2 * (self.q[1] * self.q[2] - self.q[0] * self.q[3])
        c02 = 2 * (self.q[1] * self.q[3] + self.q[0] * self.q[2])
        c10 = 2 * (self.q[1] * self.q[2] + self.q[0] * self.q[3])
        c11 = self.q[0] ** 2 - self.q[1] ** 2 + self.q[2] ** 2 - self.q[3] ** 2
        c12 = 2 * (self.q[2] * self.q[3] - self.q[0] * self.q[1])
        c20 = 2 * (self.q[1] * self.q[3] - self.q[0] * self.q[2])
        c21 = 2 * (self.q[2] * self.q[3] + self.q[0] * self.q[1])
        c22 = self.q[0] ** 2 - self.q[1] ** 2 - self.q[2] ** 2 + self.q[3] ** 2

        rotMat = np.array([[c00, c01, c02], [c10, c11, c12], [c20, c21, c22]])
        return rotMat

    def get_euler_angles(self):
        m = self.get_rot_mat()
        test = -m[2, 0]
        if test > 0.99999:
            yaw = 0
            pitch = np.pi / 2
            roll = np.arctan2(m[0, 1], m[0, 2])
        elif test < -0.99999:
            yaw = 0
            pitch = -np.pi / 2
            roll = np.arctan2(-m[0, 1], -m[0, 2])
        else:
            yaw = np.arctan2(m[1, 0], m[0, 0])
            pitch = np.arcsin(-m[2, 0])
            roll = np.arctan2(m[2, 1], m[2, 2])

        yaw = yaw*180/np.pi
        pitch = pitch*180/np.pi
        roll = roll*180/np.pi

        return yaw, pitch, roll