import math
import numpy as np
import utils
import matplotlib.pyplot as plt
from scipy.ndimage import label

class MeanShift():
    def __init__(self, max_iter=100, kernel_bandwidth=0, threshold=0.000001):
        self.kernel_bandwidth = kernel_bandwidth
        self.max_iter = max_iter
        self.threshold = threshold

    def shift_point(self, data_point, all_data_point, point_number, kernel):
        point_distances = np.zeros((point_number, 1))
        for i in range(point_number):
            point_distances[i, 0] = utils.Euclidean_Distance(data_point, all_data_point[i])
        if kernel == "Gaussian":
            point_weights = utils.Gaussian_Kernel(point_distances, self.kernel_bandwidth, point_number)
        elif kernel == "Flat":
            point_weights = utils.Flat_Kernel(point_distances, self.kernel_bandwidth, point_number)
        all_sum = 0.0
        for i in range(point_number):
            all_sum += point_weights[i, 0]

        point_shifted = point_weights.T @ all_data_point / all_sum # return (1, 2) shape
        return point_shifted

    def group_points(self, mean_shift_points):
        group_assignment = {}
        mean_shift_points = np.around(mean_shift_points,5)
        converge_point = np.unique(mean_shift_points, axis=0)
        for i in range (converge_point.shape[0]):
            for j in range (mean_shift_points.shape[0]):
                if (mean_shift_points[j][0] == converge_point[i][0]) and (mean_shift_points[j][1] == converge_point[i][1]):
                    group_assignment[j] = i

        sorted_dict = list(group_assignment.keys())
        sorted_dict.sort()
        sorted_dict = {i: group_assignment[i] for i in sorted_dict}
        group_assignment = list(sorted_dict.values())

        return group_assignment

    def fit(self, all_data_point, kernel="Gaussian"):
        mean_shift_points = np.copy(all_data_point)
        iteration = 0
        max_shifted_dist = 0.1
        point_number = np.shape(all_data_point)[0]
        need_shift = [True] * point_number

        while max_shifted_dist > self.threshold:
            max_shifted_dist = 0 # reinit the value
            iteration += 1
            for i in range(0, point_number):
                if need_shift[i] == False:
                    continue
                p_new = mean_shift_points[i]
                p_old = p_new
                p_new = self.shift_point(p_new, all_data_point, point_number, kernel)
                dist = utils.Euclidean_Distance(p_new[0], p_old)

                if dist > max_shifted_dist:
                    max_shifted_dist = dist
                if dist < self.threshold:
                    need_shift[i] = False
                mean_shift_points[i] = p_new

        group = self.group_points(mean_shift_points)  # 计算所属的类别
        all_data_point = np.array(all_data_point)
        for i in range(point_number):
            if group[i]==0:
                plt.plot(all_data_point[i, 0], all_data_point[i, 1],'ro')
            elif group[i]==1:
                plt.plot(all_data_point[i, 0], all_data_point[i, 1],'go')
            elif group[i]==2:
                plt.plot(all_data_point[i, 0], all_data_point[i, 1],'bo')
                
        mean_shift_points = np.around(mean_shift_points, 2)
        mean_shift_points = np.unique(mean_shift_points, axis=0)
        for i in range(mean_shift_points.shape[0]):
            plt.scatter(mean_shift_points[i][0], mean_shift_points[i][1], color='k', marker='*', s=150)

        plt.show() 
        return mean_shift_points
