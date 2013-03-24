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

from test_kmeans_base import *

class TestCluster(TestKMeansBase):
    def test_success_initialize(self):
        cluster = Cluster()
        assert_is_not_none(cluster)

        samples = [[1, 2, 3], 
                   [1, 3, 5],
                   [2, 4, 6],
                   [1.2, 3.21, -0.92],
                   [-0.732, 12.091, 1.098]]
        cluster.initialize([(i * 3, v) for i, v in enumerate(samples)])

    def test_success_calc_valid_centroid(self):
        cluster = Cluster()
        samples = [[1, 2, 3], 
                   [1, 3, 5],
                   [2, 4, 6],
                   [1.2, 3.21, -0.92],
                   [-0.732, 12.091, 1.098]]
        cluster.initialize([(i * 2, v) for i, v in enumerate(samples)])

        expected = [0.89359999999999995, 4.8602000000000007, 2.8356000000000003]
        centroid = cluster.calc_centroid()
        eq_(len(expected), len(centroid))
        for i, v in enumerate(centroid):
            # @todo ここの比較演算の是非は別途検討
            eq_(expected[i], v)

    def test_success_calc_valid_centroid_after_set_centroid(self):
        cluster = Cluster()
        cluster.set_centroid([0.123, -32.12, 2.983])
        
        samples = [[1, 2, 3], 
                   [1, 3, 5],
                   [2, 4, 6],
                   [1.2, 3.21, -0.92],
                   [-0.732, 12.091, 1.098]]
        cluster.initialize([(i * 7, v) for i, v in enumerate(samples)])

        expected = [0.89359999999999995, 4.8602000000000007, 2.8356000000000003]
        centroid = cluster.calc_centroid()
        eq_(len(expected), len(centroid))
        for i, v in enumerate(centroid):
            # @todo ここの比較演算の是非は別途検討
            eq_(expected[i], v)

    def test_success_set_sample_indexes(self):
        cluster = Cluster()
        samples = [[1, 2, 3], 
                   [1, 3, 5],
                   [2, 4, 6],
                   [1.2, 3.21, -0.92],
                   [-0.732, 12.091, 1.098]]
        cluster.initialize([(i * 4, v) for i, v in enumerate(samples)])

        expected = [0, 4, 8, 12, 16]
        indexes = cluster.sample_indexes
        eq_(len(expected), len(indexes))
        for i, v in enumerate(indexes):
            eq_(expected[i], v)

    def test_success_initialize_by_empty_list(self):
        cluster = Cluster()
        samples = []
        cluster.initialize([(i * 10, v) for i, v in enumerate(samples)])
        
    def test_success_calc_centroid_from_empty_list(self):
        cluster = Cluster()

        samples = []
        cluster.initialize([(i * 10, v) for i, v in enumerate(samples)])
        centroid = cluster.calc_centroid()
        ok_(centroid != centroid)

    # end of class.
