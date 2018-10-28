"""
************* Method Description ******************
Author: Satrajit Maitra
Description: Class containing methods for implementing PCA
"""

import os
import numpy as np
import gc

class PCA(object):
    def __init__(self, final_trim_pic, final_trim_sen):
        self.final_trim_pic = final_trim_pic
        self.final_trim_sen = final_trim_sen

    def normalize(self):
        mean_value = np.mean(self.final_trim_pic.astype(np.float))
        mean_value_array = np.full((3000, 4949), mean_value)
        self.final_trim_pic = np.subtract(self.final_trim_pic.astype(np.float), mean_value_array)

    def calculate_covariance(self):
        self.normalize()
        sigma = np.cov(self.final_trim_pic.T)
        return sigma

    def get_eigen_vals_vecs(self):
        sigma = self.calculate_covariance()
        eigVals, eigVec = np.linalg.eig(sigma)
        sorted_index = eigVals.argsort()[::-1]
        eigVals = eigVals[sorted_index]
        eigVec = eigVec[:,sorted_index]
        return eigVec

    def get_top_eigen_vectors(self, k):
        eigVec = self.get_eigen_vals_vecs()
        eigVec = eigVec[:,:k]
        return eigVec
