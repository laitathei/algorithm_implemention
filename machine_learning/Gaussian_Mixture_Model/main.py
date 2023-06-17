from Gaussian_Mixture_Model import GMM
from utils import *
from sklearn.mixture import GaussianMixture
from numpy import linalg

K,D,n = 2,2,10
iternation = 10
Mu, Sigma, Pi = init_params(K,D)
X = generate_sample_data(Mu, Sigma, n, K, D)
print("Raw data: ")
print(X)
test = GMM(X,K)
print("______________")
print("Init Mu:")
print(test.Mu)
print("Init Sigma:")
print(test.Sigma)
print("Init Pi:")
print(test.Pi)
print("Init Gamma:")
print(test.Gamma)
Mu, Sigma, Pi, Gamma = test.train(X,iternation)
print("______________")
print("Final Mu:")
print(Mu)
print("Final Sigma:")
print(Sigma)
print("Final Pi:")
print(Pi)
print("Final Gamma:")
print(Gamma)
# gmmsk = GaussianMixture(n_components=K, weights_init=Pi, means_init=Mu, precisions_init=linalg.inv(Sigma), max_iter=iternation)
# gmmsk.fit(X)
# print("______________")
# print("pkg Mu:")
# print(gmmsk.means_)
# print("pkg Sigma:")
# print(gmmsk.covariances_)
# print("pkg Pi:")
# print(gmmsk.weights_)