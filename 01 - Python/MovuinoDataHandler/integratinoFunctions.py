import numpy as np


def Euler(T, A, y0):
    Y = [y0]
    for i in range(len(T)-1):
        pas = T[i+1]-T[i]
        yt1 = A[i]*pas*0.001 + Y[i]
        Y.append(yt1)

    return Y
"""
def Offset(L):
    offset = L[0]
    for i in range(len(L)):
        L[i] =L[i]-offset
    return L
"""


def EuclidienNorm(V):
    norm = 0
    for i in range(len(V)):
        norm += V[0]**2
    return np.sqrt(norm)

def EuclidienNormListVector(listV):
    """
    Return a list a the norm of the list of vectors V for each tTime
    :param V:
    :return:
    """
    listNorm = []

    for i in range(len(listV[0])):
        V = [0]*3
        V[0] = listV[0][i]
        V[1] = listV[1][i]
        V[2] = listV[2][i]
        listNorm.append(EuclidienNorm(V))
    print(listNorm)
    return listNorm