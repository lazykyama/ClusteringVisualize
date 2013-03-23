#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class RandDataGenerator:

    def __init__(self, size = 100, dim = 3): 
        self.size = size
        self.dim  = dim

        # Mersenne Twister.
        self.rs   = np.random.RandomState()
        
    def generate_multivariate_norm(self, mean = None, cov = None, size = None):

        if mean is None or cov is None: 
            raise TypeError('generate_multivariate_norm() takes at least 2 positional arguments.')
        
        exec_size = self.size
        if size is not None and size > 0: 
            exec_size = size

        return self.rs.multivariate_normal(mean, cov, exec_size)

    # 当面何もしない
    def generate_multivariate_random_mean(self, dim = None):
        pass

    # 当面何もしない
    def generate_multivariate_random_cov(self, dim = None):
        pass
