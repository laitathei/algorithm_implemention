import numpy as np

def generate_sample_data(mean: list, std: list, N: int, K: int, D: int):
    """
    Generate Generate random samples of data points
    mean: mean of each cluster
    std: standard deviation of each cluster
    N: number of data point generated
    K: number of cluster
    D: dimension of data point
    """
    # Prepare empty array to store the generated data point
    samples = np.empty((N, D))

    # Generate normal distribution
    for i in range (K):
        n = int(N / K)
        samples[n * i:n * (i + 1)] = np.random.multivariate_normal(mean=mean[i], cov=std[i] ** 2, size=n)
    return samples

def init_params(K, D):
    Mu = np.random.uniform(-10,10,(K, D)) # K*D
    Sigma = np.zeros((K,D,D)) # K*D*D
    for i in range(Sigma.shape[0]):
        Sigma[i] = np.eye(D) * np.random.uniform(0,1)
    Pi = np.array([1.0 / K] * K) # K
    return Mu, Sigma, Pi