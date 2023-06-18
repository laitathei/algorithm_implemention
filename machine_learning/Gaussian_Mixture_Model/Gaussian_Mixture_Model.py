import numpy as np
import seaborn as sns
from utils import *
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal
from numpy import inf, linalg

class GMM(object):
    def __init__(self, X, K):
        self.data = X
        self.N, self.D = X.shape
        self.K = K
        self.Mu, self.Sigma, self.Pi, self.Gamma = self.init_params()
        self.minimum_error = 1e-6
        self.sum_log_list = []
        self.step_list = []
        if self.D == 1:
            self.plot_1D(-1)
        elif self.D == 2:
            self.plot_2D(-1)
        elif self.D == 3:
            self.plot_3D(-1)

    def init_params(self):
        Mu = np.random.uniform(-10,10,(self.K, self.D)) # K*D
        Sigma = np.zeros((self.K,self.D,self.D)) # K*D*D
        for i in range(Sigma.shape[0]):
            Sigma[i] = np.eye(self.D) * np.random.uniform(0.5,1)
        Pi = np.array([1.0 / self.K] * self.K) # K
        Gamma = np.random.dirichlet(np.ones(self.K),size=(self.N)) # N*K
        return Mu, Sigma, Pi, Gamma
    
    def E_step(self, X, step):
        prob = []
        for i in range(self.K):
            if linalg.det(self.Sigma[i]) == 0:
                self.Sigma[i] = np.zeros((len(np.diag(self.Sigma[i])),len(np.diag(self.Sigma[i]))))
                for j in range (len(np.diag(self.Sigma[i]))):
                    self.Sigma[i][j][j] = self.minimum_error
                self.Mu[i] = np.zeros(self.D)
            prob.append(multivariate_normal(self.Mu[i], self.Sigma[i], allow_singular=True).pdf(X))

        # Prepare Probability Density Function of Gaussian Distribution of each data point
        # shape(Number of Point, Number of Cluster)
        prob = np.array(prob).T

        # weight each point with corresponding cluster
        # shape(Number of Point, Number of Cluster) * shape(Number of Cluster)

        Pi_Gussian = prob * self.Pi
        # sum each row which means the probability of all weighted cluster 
        # shape(Number of Cluster)
        sum_K = np.sum(Pi_Gussian, axis=1)

        # Record the previous log likelihood
        log_likelihood_prev = np.log(self.Gamma)
        log_likelihood_prev[log_likelihood_prev == -inf] = 0 # replace -inf to be 0
        sum_log_likelihood_prev = np.sum(log_likelihood_prev)

        # Calculate the probability of each datapoint that belongs to cluster c
        # shape(Number of Point, Number of Cluster)
        r = (Pi_Gussian.T / sum_K).T

        # Calculate the log likelihood
        log_likelihood = np.log(r)
        log_likelihood[log_likelihood == -inf] = 0 # replace -inf to be 0
        sum_log_likelihood = np.sum(log_likelihood)

        if sum_log_likelihood == 0: # indicates the probability that each point has been found to belong to its cluster with 100% sure
            sum_log_likelihood = sum_log_likelihood_prev

        diff = sum_log_likelihood - sum_log_likelihood_prev

        # save for draw graph
        self.sum_log_list.append(sum_log_likelihood)
        self.step_list.append(step)

        # Map each data point to each cluster by selecting the largest probability
        # shape(Number of Cluster)
        label = np.argmax(np.array(r), axis=1)
        cluster = {}.fromkeys(([i for i in range (self.K)]))
        for i in range (len(label)):
            for j in range (self.K):
                if label[i] == j:
                    if cluster[j] is None:
                        cluster[j] = [list(self.data[i])]
                    else:
                        cluster[j].append(list(self.data[i]))
        return r, cluster, diff
    
    def M_step(self, X, step):
        # sum each cluster data point probability
        # shape(Number of Cluster)
        m = np.sum(self.Gamma, axis=0)

        # multiply with all data point
        # shape(Number of Cluster, Number of Dimension)
        mx = (self.Gamma.T @ X)

        # replace inf to 0
        one_divide_m = 1/m
        one_divide_m[one_divide_m == inf] = 0

        # Get new means
        # shape(Number of Cluster, Number of Dimension)
        newMu = (one_divide_m * mx.T).T

        # Get new weight
        # shape(Number of Cluster)
        newPi = m / self.N

        # get new Sigma
        newSigma = []
        for i in range(self.K):
            # (1/m)[i] 
            # weight of Cluster

            # self.Gamma[:, i] 
            # probability of each datapoint that belongs to cluster c
            # shape(Number of Point)

            # (self.Gamma[:, i] * (X - newMu[i]).T) 
            # probability of each datapoint that belongs to cluster c multiply with new shift between data point and new means
            # shape(Number of Dimension, Number of Point)

            # (X - newMu[i]) 
            # new shift between data point and new means
            # shape(Number of Point, Number of Dimension)
            newSigma.append((one_divide_m)[i] * np.dot((self.Gamma[:, i] * (X - newMu[i]).T), (X - newMu[i])))

        # newSigma shape(Number of Cluster, Number of Dimension, Number of Dimension)
        newSigma = np.array(newSigma)
        return newMu, newSigma, newPi

    def train(self, X, total_step):
        plt.ion()
        for i in range(total_step):
            self.Gamma, cluster, diff = self.E_step(X, i)
            self.Mu, self.Sigma, self.Pi = self.M_step(X, i)
            if abs(diff) < self.minimum_error:
                print("Step of just fit: ", i)
                interrupt = True
                self.plot_graph(i, total_step, cluster, interrupt)
                break
            else:
                self.plot_graph(i, total_step, cluster)
        return self.Mu, self.Sigma, self.Pi, self.Gamma

    def plot_graph(self, i, total_step, cluster, interrupt=False):
        if self.D == 1:
            self.plot_1D(i, total_step, interrupt)
        elif self.D == 2:
            self.plot_2D(i, total_step, cluster, interrupt)
        elif self.D == 3:
            self.plot_3D(i, total_step, cluster, interrupt)

    def plot_1D(self, current_step, total_step=None, interrupt=False):
        for i in range (self.K):
            # Plot the guess data
            X = norm.rvs(self.Mu[i], self.Sigma[i][0], size=1000)
            plt.hist(X, bins=50, density=True, alpha=0.5)
            # Plot the guess PDF
            x = np.linspace(X.min(), X.max(), 1000)
            y = norm.pdf(x, self.Mu[i], self.Sigma[i][0])
            plt.plot(x, y, linestyle='--', color="black")
            # Plot the scatter of true data
            plt.scatter(self.data, [0]*self.N, color='k')

        if current_step == -1:
            # Plot the guess data and PDF for init process
            plt.title("Random Init")
            plt.savefig("Random Init.png",bbox_inches='tight')
            self.xmin, self.xmax, self.ymin, self.ymax = plt.axis()
        else:
            # Plot the guess data and PDF for each step
            plt.xlim([self.xmin, self.xmax])
            plt.ylim([self.ymin, self.ymax])
            plt.title("Step: {}".format(current_step))
            if interrupt == True:
                plt.savefig("Final Step.png",bbox_inches='tight')
            if current_step == total_step-1:
                plt.savefig("Final Step.png",bbox_inches='tight')
        plt.show()
        plt.pause(0.5)
        plt.clf()

    def plot_2D(self, current_step, total_step=None, cluster=None, interrupt=False):
        colors = ["c", "b", "g", "r", "m", "y", "k", "w"] # currently support for 8 cluster
        if current_step >= 0:
            plt.title("Step: {}".format(current_step))
            # Plot the scatter of guess data and the gaussian curve of guess data for each step
            for i in range (len(cluster)):
                if cluster[i] != None:
                    x = np.array(cluster[i])[:,0]
                    y = np.array(cluster[i])[:,1]
                    sns.kdeplot(x=x, y=y, levels=20, color='k', alpha=0.1)
                    plt.scatter(x, y, c=colors[i])
            plt.xlim([self.xmin, self.xmax])
            plt.ylim([self.ymin, self.ymax])
            if interrupt == True:
                plt.savefig("Final Step.png",bbox_inches='tight')
            if current_step == total_step-1:
                plt.savefig("Final Step.png",bbox_inches='tight')
            plt.show()
            plt.pause(0.5)
            plt.clf()
        else:
            # Plot scatter of true data and the gaussian curve of true data for init process
            x = self.data[:,0]
            y = self.data[:,1]
            sns.kdeplot(x=x, y=y, levels=20, color='k', alpha=0.1)
            self.xmin, self.xmax, self.ymin, self.ymax = plt.axis()
            plt.scatter(x, y)
            plt.title("Random Init")
            plt.savefig("Random Init.png",bbox_inches='tight')
            plt.show()
            plt.pause(0.5)
            plt.clf()

    def plot_3D(self, current_step, total_step=None, cluster=None, interrupt=False):
        colors = ["c", "b", "g", "r", "m", "y", "k", "w"] # currently support for 8 cluster
        max_list = np.max(self.data, axis=0)
        min_list = np.min(self.data, axis=0)
        axes = plt.axes(projection='3d')
        axes.set_xlim([min_list[0], max_list[0]])
        axes.set_ylim([min_list[1], max_list[1]])
        axes.set_zlim([min_list[2], max_list[2]])
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.set_zlabel('Z')
        if current_step >= 0:
            plt.title("Step: {}".format(current_step))
            # Plot the scatter guess for each step
            for i in range(len(cluster)):
                if cluster[i] != None:
                    axes.scatter(np.array(cluster[i])[:,0], np.array(cluster[i])[:,1], np.array(cluster[i])[:,2], alpha=1, c=colors[i])
            plt.xlim([self.xmin, self.xmax])
            plt.ylim([self.ymin, self.ymax])
            if interrupt == True:
                plt.savefig("Final Step.png",bbox_inches='tight')
                plt.figure()
                plt.plot(self.step_list, self.sum_log_list)
                plt.xticks(self.step_list)
                plt.xlabel("Step")
                plt.ylabel("Log")
                plt.title("Log likelihood")
                plt.savefig("Log likelihood.png",bbox_inches='tight')
                plt.show()
                plt.pause(0.5)
                plt.clf()
            if current_step == total_step-1:
                plt.savefig("Final Step.png",bbox_inches='tight')
                plt.figure()
                plt.plot(self.step_list, self.sum_log_list)
                plt.xticks(self.step_list)
                plt.xlabel("Step")
                plt.ylabel("Log")
                plt.title("Log likelihood")
                plt.savefig("Log likelihood.png",bbox_inches='tight')
                plt.show()
                plt.pause(0.5)
                plt.clf()
        else:
            # Plot the scatter of true for init process
            axes.scatter(self.data[:,0], self.data[:,1], self.data[:,2], alpha=1, c='k')
            self.xmin, self.xmax, self.ymin, self.ymax = plt.axis()
            plt.title("Random Init")
            plt.savefig("Random Init.png",bbox_inches='tight')
        plt.show()
        plt.pause(0.5)
        plt.clf()
