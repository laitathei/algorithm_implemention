import numpy as np
import math
import random

class kf:
    def __init__(self, states_num: int, meas_num: int, input_num: int, dt: float, std_acc: float, x_std_meas: float, y_std_meas: float, noise: float):
        """
        :param states_num: number of state variable
        :param meas_num: number of measure variable
        :param input_num: number of control input variable
        :param dt: sampling time (time for 1 cycle)
        :param std_acc: process noise standard deviation
        :param x_std_meas: standard deviation of the measurement in x-direction
        :param y_std_meas: standard deviation of the measurement in y-direction
        :param noise: random noise range in process and measurement

        x is state vector
        z is measurement vector
        F is state transition matrix
        u is control input vector
        G is control matrix
        P is covariance matrix of the estimation error
        Q is covariance matrix of the process noise
        R is covariance matrix of the measurement
        w is process noise vector (an unmeasurable input that affects the state)
        v is measurement noise vector (an unmeasurable noise that affects the measurement)
        H is observation matrix
        K is kalmen gain
        """
        
        # all notation reference to https://www.kalmanfilter.net/multiSummary.html
        self.states_num = states_num
        self.meas_num = meas_num
        self.input_num = input_num

        self.x = np.zeros((self.states_num,1))
        self.z = np.zeros((self.meas_num,1))
        self.F = np.zeros((self.states_num,self.states_num))
        self.u = np.zeros((self.input_num,1))
        self.G = np.zeros((self.states_num,self.input_num))
        self.P = np.zeros((self.states_num,self.states_num))
        self.Q = np.zeros((self.states_num,self.states_num))
        self.R = np.zeros((self.meas_num,self.meas_num))
        self.H = np.zeros((self.meas_num,self.states_num))
        self.K = np.zeros((self.states_num,self.meas_num))
        self.w = np.zeros((self.states_num,1))
        self.v = np.zeros((self.meas_num,1))

        self.F = np.array([[1,0,dt,0],
                            [0,1,0,dt],
                            [0,0,1,0],
                            [0,0,0,1]])
        self.u = np.array([[0],
                            [0]])
        self.G = np.array([[0.5 * dt**2, 0],
                           [0, 0.5 * dt**2],
                           [dt, 0],
                           [0, dt]])
        self.P = np.eye(states_num)
        self.Q = self.G @ self.G.T * std_acc**2
        self.R = np.array([[x_std_meas**2,0],
                           [0, y_std_meas**2]])
        self.H = np.array([[1,0,0,0],
                           [0,1,0,0]])
        self.w = np.array([[random.uniform(noise,-noise)],
                           [random.uniform(noise,-noise)],
                           [random.uniform(noise,-noise)],
                           [random.uniform(noise,-noise)]])
        self.v = np.array([[random.uniform(noise,-noise)],
                           [random.uniform(noise,-noise)]])
        assert self.F.shape == (self.states_num,self.states_num), "Wrong state transition matrix shape"
        assert self.u.shape == (self.input_num,1), "Wrong control input vector shape"
        assert self.G.shape == (self.states_num,self.input_num), "Wrong control matrix shape"
        assert self.P.shape == (self.states_num,self.states_num), "Wrong covariance matrix of the estimation error shape"
        assert self.Q.shape == (self.states_num,self.states_num), "Wrong covariance matrix of the process noise shape"
        assert self.R.shape == (self.meas_num,self.meas_num), "Wrong covariance matrix of the measurement shape"
        assert self.H.shape == (self.meas_num,self.states_num), "Wrong observation matrix shape"
        assert self.w.shape == (self.states_num,1), "Wrong process noise vector shape"
        assert self.v.shape == (self.meas_num,1), "Wrong measurement noise vector shape"

        self.predict(self.u)

    def predict(self, u: np.array) -> None:
        """
        Extrapolate the state
        x = F x + G u + w (optional)

        Extrapolate uncertainty (with discrete or continuous noise model)
        P = F P F.T + Q

        Extrapolate uncertainty (with control input)
        P = F P F.T + G G.T std**2

        Extrapolate uncertainty (without control input)
        P = F P F.T + F F.T Qa

        P is covariance matrix of the estimation error
        F is state transition matrix
        Q is covariance matrix of the process noise
        G is control matrix
        u is control input vector
        std is random standard deviation of control input
        """
        self.u = u
        self.x = self.F @ self.x + self.G @ self.u
        self.P = self.F @ self.P @ self.F.T + self.Q

        assert self.x.shape == (self.states_num,1), "Wrong state vector shape in predict process"
        assert self.P.shape == (self.states_num,self.states_num), "Wrong covariance matrix of the estimation error shape in predict process"

        return self.x[0:2]

    def update(self, z: np.array):
        """
        Compute the Kalmen Gain
        K = P H.T (H P H.T + R)^-1

        Update estimate with measurement
        x = x + K (z - H x - v (optional))

        Update the estimate uncertainty
        P = (I - K H) P (I - K H).T + K R K.T

        K is kalmen gain
        H is observation matrix
        R is covariance matrix of the measurement
        z is measurement vector
        I is identity matrix
        """
        self.z = z
        self.K = self.P @ self.H.T @ (np.linalg.inv(self.H @ self.P @ self.H.T + self.R))
        self.x = self.x + self.K @ (self.z - self.H @ self.x - self.v)
        I = np.eye(self.states_num)
        self.P = (I - self.K @ self.H) @ self.P @ (I - self.K @ self.H).T + self.K @ self.R @ self.K.T

        assert self.z.shape == (self.meas_num,1), "Wrong measurement vector shape in update process"
        assert self.K.shape == (self.states_num,self.meas_num), "Wrong kalmen gain shape in update process"
        assert self.x.shape == (self.states_num,1), "Wrong state vector shape in update process"
        assert self.P.shape == (self.states_num,self.states_num), "Wrong covariance matrix of the estimation error shape in update process"
        
        return self.x[0:2]
    