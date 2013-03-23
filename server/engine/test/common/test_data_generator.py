#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インクルードに絡むおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/common'))

import unittest
from nose.tools import *

import data_generator

class TestRandDataGenerator(unittest.TestCase):

    def test_create_multivariate_norm_success(self): 
        rd_gen = data_generator.RandDataGenerator()
        assert_is_not_none(rd_gen)

        mean = [1,1,1]
        cov  = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        size = 10
        sample = rd_gen.generate_multivariate_norm(mean, cov, size)
        assert_is_not_none(sample)

        print ''
        print 'sample: '
        print sample

if __name__ == '__main__':
    unittest.main()

