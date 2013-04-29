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

import numpy as np

class TestKMeansBase(unittest.TestCase):
    MEAN  = np.array([1,1,1])
    COV   = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    SCALE = 1.0
    SIZE  = 10

    # util method.
    def create_test_random_samples(self, mean = None, cov = None,
                                   scale = None, size = None):
        sample_mean = TestKMeansBase.MEAN
        sample_cov  = TestKMeansBase.COV
        sample_scale = TestKMeansBase.SCALE
        sample_size = TestKMeansBase.SIZE
        if mean is not None:
            sample_mean = mean
        if cov is not None:
            sample_cov = cov
        if scale is not None:
            sample_scale = scale
        if size is not None:
            sample_size = size

        scaled_cov = sample_scale * sample_cov
            
        rd_gen = data_generator.RandDataGenerator()
        samples = rd_gen.generate_multivariate_norm(
            sample_mean, scaled_cov, sample_size)
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
        
