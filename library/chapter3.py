import cv2
import numpy as np

# Chapter 3 functions

L = 256

def Negative(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            s = L - 1 - r
            imgout[x, y] = np.uint8(s)
    return imgout

def Power(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    gamma = 5.0
    c = np.power(L - 1.0, 1 - gamma)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r == 0:
                r = 1
            s = c * np.power(1.0 * r, gamma)
            imgout[x, y] = np.uint8(s)
    return imgout

def NegativeColor(imgin):
    M, N, C = imgin.shape
    imgout = np.zeros((M, N, C), np.uint8)
    for x in range(0, M):
        for y in range(0, N):
            b = imgin[x, y, 0]
            g = imgin[x, y, 1]
            r = imgin[x, y, 2]
            b = L - 1 - b
            g = L - 1 - g
            r = L - 1 - r
            imgout[x, y, 0] = np.uint8(b)
            imgout[x, y, 1] = np.uint8(g)
            imgout[x, y, 2] = np.uint8(r)
    return imgout

def Logarit(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    c = (L - 1.0)/np.log(1.0*L)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r == 0:
                r = 1
            s = c*np.log(1.0 + r)
            imgout[x, y] = np.uint8(s)
    return imgout

def PiecewiseLine(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    rmin, rmax, _, _ = cv2.minMaxLoc(imgin)
    smin = 0
    smax = L - 1
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r < rmin:
                s = 1.0 * smin / rmin * r
            elif r < rmax:
                s = 1.0 * (smax - smin) / (rmax - rmin) * (r - rmin) + smin
            else:
                s = 1.0 * (L - 1 - smax) / (L - rmax) * (r - rmax) + smax
            imgout[x, y] = np.uint8(s)
    return imgout

def histogram(imgin):
    M, N = imgin.shape
    imgout = np.zeros((L, L, 3), np.uint8) + np.uint8(255)
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1
    p = 1.0 * h / (M * N)
    scale = 3000
    for r in range(0, L):
        cv2.line(imgout, (r, 0), (r, L - np.int32(scale * p[r])), (0, 0, 255))
    return imgout

def HisEqual(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1
    p = 1.0 * h / (M * N)
    s = np.zeros(L, np.float64)
    for k in range (0, L):
        for j in range (0, k + 1):
            s[k] = s[k] + p[j]
            h = np.zeros(L, np.int32)
    for x in range (0, M):
        for y in range (0, N):
            r = imgin[x, y]
            imgout [x, y] = np.uint8((L - 1) * s[r])
    return imgout

def localHist(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    for x in range(a, M - a):
        for y in range(b, N - 1):
            w = imgin[x - a: x + a + 1, y - b: y + b + 1]
            w = cv2.equalizeHist(w)
            imgout[x, y] = w[a, b]
    return imgout

def histStat(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    mean, stddev = cv2.meanStdDev(imgin)
    mG = mean[0, 0]
    sigmaG = stddev[0, 0]
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    c = 22.8
    k0 = 0.0
    k1 = 0.1
    k2 = 0.0
    k3 = 0.1
    for x in range(a, M - a):
        for y in range(b, N - 1):
            w = imgin[x - a: x + a + 1, y - b: y + b + 1]
            mean, stddev = cv2.meanStdDev(w)
            msxy = mean[0, 0]
            sigmasxy = stddev[0, 0]
            if (k0 * mG <= msxy <= k1 * mG) and (k2 * sigmaG <= sigmasxy <= k3 * sigmaG):           
                imgout[x, y] = np.uint8(c * imgin[x, y])
            else:
                imgout[x, y] = imgin[x, y]
    return imgout

def Sharp(imgin):
    w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], np.float32)
    laplacian = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    imgout = imgin - laplacian
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def Gradient(imgin):
    sobel_x = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    sobel_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    gx = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_x)
    gy = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_y)
    imgout = abs(gx) + abs(gy)
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def phan_nguong(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r > 63:
                s = 255
            else:
                s = 0
            imgout[x, y] = np.uint8(s)
    imgout = cv2.medianBlur(imgout, 7)
    return imgout