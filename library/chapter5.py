import numpy as np

# Chapter 5 functions

L = 256

def FrequencyFiltering(imgin, H):
    f = imgin.astype(np.float64)
    F = np.fft.fft2(f)
    F = np.fft.fftshift(F)
    G = F * H
    G = np.fft.ifftshift(G)
    g = np.fft.ifft2(G)
    gR = g.real.copy()
    gR = np.clip(gR, 0, L - 1)
    imgout = gR.astype(np.uint8)
    return imgout

def CreateMotionFilter(M, N):
    H = np.zeros((M, N), np.complex64)
    a = 0.1
    b = 0.1
    T = 1.0
    phi_pre = 0
    for u in range(M):
        for v in range(N):
            phi = np.pi * ((u - M // 2) * a + (v - N // 2) * b)
            if abs(phi) < 1.0e-6:
                phi = phi_pre
            RE  = T * np.sin(phi) / phi * np.cos(phi)
            IM  = T * np.sin(phi) / phi * np.sin(phi)
            H.real[u, v] = RE
            H.imag[u, v] = IM
            phi_pre = phi
    return H

def CreateMotion(imgin):
    M, N = imgin.shape
    H = CreateMotionFilter(M, N)
    imgout = FrequencyFiltering(imgin, H)
    return imgout

def CreateInverseMotionFilter(M, N):
    H = np.zeros((M, N), np.complex64)
    a = 0.1
    b = 0.1
    T = 1.0
    phi_pre = 0.0
    
    for u in range(M):
        for v in range(N):
            phi = np.pi * ((u - M // 2) * a + (v - N // 2) * b)
            mau_so = np.sin(phi)  
            if (abs(mau_so) < 1.0e-6):
                phi = phi_pre
            RE = phi / (T * np.sin(phi)) * np.cos(phi)
            IM = phi / T   
            H.real[u, v] = RE
            H.imag[u, v] = IM
            phi_pre = phi
    return H

def DeMotion(imgin):
    M, N = imgin.shape
    H = CreateInverseMotionFilter(M, N)
    imgout = FrequencyFiltering(imgin, H)
    return imgout