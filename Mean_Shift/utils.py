import math
import numpy as np
import cv2
from matplotlib import pyplot as plt

def Euclidean_Distance(pointA, pointB):
    ans = ((pointA[0] - pointB[0])**2+(pointA[1] - pointB[1])**2)**0.5
    return ans

def Flat_Kernel(distance, bandwidth, point_number):
    inRange = []
    weight = np.zeros((point_number, 1))
    for i in range (distance.shape[0]):
        if distance[i] <= bandwidth:
            inRange.append(distance[i])
            weight[i] = 1
    inRange = np.array(inRange)
    print(inRange)
    return weight

def Gaussian_Kernel(distance, bandwidth, point_number):
    left = 1.0/(bandwidth * math.sqrt(2*math.pi))
    right = np.zeros((point_number, 1))  # mX1的矩阵
    for i in range(point_number):
        right[i, 0] = (-0.5 * distance[i] * distance[i]) / (bandwidth * bandwidth)
        right[i, 0] = np.exp(right[i, 0])
    return left * right

def Get_Mono_Histogram(image_dir):
    img = cv2.imread(image_dir)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()
    print(hist)

def Get_RGB_Histogram(image_dir):
    img = cv2.imread(image_dir)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()