from MeanShift import MeanShift
from utils import *

X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8 ],
              [8, 8],
              [1, 0.6],
              [9,11],
              [8,2],
              [10,2],
              [9,3],])

meanshift = MeanShift(100, 4, 0.000001)
converge_point = meanshift.fit(X, kernel="Flat")
print(converge_point)