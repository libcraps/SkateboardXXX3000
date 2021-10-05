import numpy as np
import math


def EulerIntegration(Uprime, dt):
    """

    :param Uprime:
    :param dt:
    :return:
    """
    U = [np.array([0, 0, 0])]
    n = len(Uprime)
    for k in range(n - 1):
        Ux = Uprime[k][0] * dt + U[k][0]
        Uy = Uprime[k][1] * dt + U[k][1]
        Uz = Uprime[k][2] * dt + U[k][2]
        U.append(np.array([Ux, Uy, Uz]))
    return U



def Euler(T, A, y0):
    Y = [y0]
    for i in range(len(T)-1):
        pas = T[i+1]-T[i]
        yt1 = A[i]*pas*0.025 + Y[i]
        Y.append(yt1)

    return Y
"""
def Offset(L):
    offset = L[0]
    for i in range(len(L)):
        L[i] =L[i]-offset
    return L
"""


def EuclidienNorm(V) :
    norm = 0
    for i in range(len(V)):
        norm += V[i]**2
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
    return listNorm

def G(n,fc,f):
    return 1.0/math.sqrt(1+(f/fc)**(2*n))