import numpy as np


def Euler(T, A, y0):
    Y = [y0]
    for i in range(len(T)-1):
        pas = T[i+1]-T[i]
        yt1 = A[i]*pas*0.001 + Y[i]
        Y.append(yt1)

    return Y

def Offset(L):
    offset = L[0]
    for i in range(len(L)):
        L[i] =L[i]-offset
    return L