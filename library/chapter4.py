import numpy as np
import cv2

# Chapter 4 functions

L = 256

def Spectrum(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = 1.0 * imgin / (L - 1)
    
    for x in range(0, M):
        for y in range(0, N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]
                
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    FR = F[:, :, 0]
    FI = F[:, :, 1]
    S = np.sqrt(FR * FR + FI * FI)
    S = np.clip(S, 0, L - 1)
    imgout = S.astype(np.uint8)
    return imgout

def RemoveMoireSimple(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = 1.0 * imgin
    
    for x in range(0, M):
        for y in range(0, N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]
                
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    FR = F[:, :, 0]
    FI = F[:, :, 1]
    H = CreateMoireFilter(P, Q)
    G = cv2.mulSpectrums(F, H, flags=cv2.DFT_ROWS)
    g = cv2.idft(G, flags=cv2.DFT_SCALE)
    gR = g[:M, :N, 0]
    for x in range(0, M):
        for y in range(0, N):
            if (x + y) % 2 == 1:
                gR[x, y] = -gR[x, y]
    gR = np.clip(gR, 0, L - 1)
    imgout = gR.astype(np.uint8)
    return imgout
    
def CreateMoireFilter(P, Q):
    H = np.ones((P, Q, 2), np.float32)
    H[:, :, 1] = 0.0
    u1 = 45; v1 = 58
    u2 = 86; v2 = 58
    u3 = 41; v3 = 119
    u4 = 83; v4 = 119
    
    u5 = P-u1; v5 = Q-v1
    u6 = P-u2; v6 = Q-v2
    u7 = P-u3; v7 = Q-v3
    u8 = P-u4; v8 = Q-v4
    
    D0 = 15
    for u in range(0, P):
        for v in range(0, Q):
            Duv = np.sqrt((u-u1)*(u-u1) + (v-v1)*(v-v1))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u2)*(u-u2) + (v-v2)*(v-v2))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u3)*(u-u3) + (v-v3)*(v-v3))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u4)*(u-u4) + (v-v4)*(v-v4))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u5)*(u-u5) + (v-v5)*(v-v5))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u6)*(u-u6) + (v-v6)*(v-v6))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u7)*(u-u7) + (v-v7)*(v-v7))
            if Duv < D0:
                H[u, v, 0] = 0.0
                
            Duv = np.sqrt((u-u8)*(u-u8) + (v-v8)*(v-v8))
            if Duv < D0:
                H[u, v, 0] = 0.0
    return H

def CreateNotchInterferenceFilter(P, Q):
    H = np.ones((P, Q, 2), np.float32)
    H[:, :, 1] = 0.0
    D0 = 10
    V0 = Q //2
    for u in range(0, P):
        for v in range(0, Q):
            if u not in range(P // 2 - 10, P // 2 + 10 + 1):
                if abs(v - V0) <= D0:
                    H[u, v, 0] = 0.0
    return H

def DrawNotchFilter(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    H = CreateMoireFilter(P, Q)
    HR = H[:, :, 0] * (L - 1)
    imgout = HR.astype(np.uint8)
    return imgout
    
def RemovePeriodNoise(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = 1.0 * imgin
    
    for x in range(0, M):
        for y in range(0, N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]
                
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    FR = F[:, :, 0]
    FI = F[:, :, 1]
    H = CreateNotchInterferenceFilter(P, Q)
    G = cv2.mulSpectrums(F, H, flags=cv2.DFT_ROWS)
    g = cv2.idft(G, flags=cv2.DFT_SCALE)
    gR = g[:M, :N, 0]
    for x in range(0, M):
        for y in range(0, N):
            if (x + y) % 2 == 1:
                gR[x, y] = -gR[x, y]
    gR = np.clip(gR, 0, L - 1)
    imgout = gR.astype(np.uint8)
    return imgout
