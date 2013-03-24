#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インクルードに絡むおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/kmeans'))

import unittest
from nose.tools import *

import data_generator
from kmeans import *

class TestKMeansBase(unittest.TestCase):
    MEAN = [1,1,1]
    COV  = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    SIZE = 10

    # util method.
    def create_test_random_samples(self):
        rd_gen = data_generator.RandDataGenerator()
        samples = rd_gen.generate_multivariate_norm(
            TestKMeansBase.MEAN, TestKMeansBase.COV,
            TestKMeansBase.SIZE)
        return samples

    def create_test_mixture_random_samples(self, k = 3):
        rd_gen = data_generator.RandDataGenerator()
        each_size = 30
        radius = 10
        each_mean_list = [[0,
                           radius * np.sin(2 * np.pi * i / k),
                           radius * np.cos(2 * np.pi * i / k)]
                          for i in range(k)]
        samples_list = [rd_gen.generate_multivariate_norm(
                m, TestKMeansBase.COV, each_size).tolist()
                        for m in each_mean_list]
        samples = np.array(reduce(lambda a, b: a + b, samples_list))
        return samples
        
