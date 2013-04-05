#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インポートに絡むおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/kmeans'))

import unittest
from nose.tools import *

import numpy as np

import data_generator
from kmeans import *

from test_kmeans_base import *

from scipy.cluster.vq import vq, kmeans, whiten

class TestKMeans(TestKMeansBase):
    # 初期化できること
    def test_success_initialize(self):
        kmeans_instance = KMeans()
        assert_is_not_none(kmeans_instance)

        samples = self.create_test_random_samples()
        kmeans_instance.set_samples(samples)
        eq_(TestKMeans.SIZE, kmeans_instance.get_samples_size())

    # 学習に成功すること
    def test_success_learning_completely(self):
        kmeans_instance = KMeans()
        samples = self.create_test_random_samples()
        kmeans_instance.set_samples(samples)

        # 学習結果の是非については、ここでは確認しない
        ok_(kmeans_instance.learn())
        ok_(not kmeans_instance.learn())

    # 初期割り当てを指定して学習に成功すること
    def test_success_learning_completely_with_set_init_assigns(self):
        kmeans_instance = KMeans()
        samples = self.create_test_random_samples()
        kmeans_instance.set_samples(samples)

        # 初期割り当てを実施
        rand_assigns = KMeans.generate_random_assigns(
            kmeans_instance.k, len(samples))
        kmeans_instance.set_init_assign(rand_assigns)

        # 学習結果の是非については、ここでは確認しない
        ok_(kmeans_instance.learn())
        ok_(not kmeans_instance.learn())

    # 適切に学習されること
    def test_success_valid_learning(self):
        K = 3
        kmeans_instance = KMeans(k = K)
        samples = np.array([[77.3,13.0,9.7,1.5,6.4],
                            [82.5,10.0,7.5,1.5,6.5],
                            [66.9,20.6,12.5,2.3,7.0],
                            [47.2,33.8,19.0,2.8,5.8],
                            [65.3,20.5,14.2,1.9,6.9],
                            [83.3,10.0,6.7,2.2,7.0],
                            [81.6,12.7,5.7,2.9,6.7],
                            [47.8,36.5,15.7,2.3,7.2], 
                            [48.6,37.1,14.3,2.1,7.2],
                            [61.6,25.5,12.9,1.9,7.3],
                            [58.6,26.5,14.9,2.4,6.7],
                            [69.3,22.3,8.4,4.0,7.0],
                            [61.8,30.8,7.4,2.7,6.4],
                            [67.7,25.3,7.0,4.8,7.3],
                            [57.2,31.2,11.6,2.4,6.5],
                            [67.2,22.7,10.1,3.3,6.2],
                            [59.2,31.2,9.6,2.4,6.0],
                            [80.2,13.2,6.6,2.0,5.8],
                            [82.2,11.1,6.7,2.2,7.2],
                            [69.7,20.7,9.6,3.1,5.9]])
        init_centroid = [np.array([82.5,10.0,7.5,1.5,6.5]),
                         np.array([47.8,36.5,15.7,2.3,7.2]),
                         np.array([67.2,22.7,10.1,3.3,6.2])]
        
        kmeans_instance.set_samples(samples)
        kmeans_instance.set_centroids(init_centroid)
        ok_(kmeans_instance.learn())

        # answer is np.kmeans
        book = np.array(([82.5,10.0,7.5,1.5,6.5], 
                         [47.8,36.5,15.7,2.3,7.2], 
                         [67.2,22.7,10.1,3.3,6.2]))
        np_kmeans_results = kmeans(samples, book)
        answer = np.array([np.argmin(np.sum((d - np_kmeans_results[0]) ** 2,
                                   axis = 1)) 
                  for d in samples])
        answer_each_size = [np.sum(answer == k) for k in range(K)]

        actual_each_size = kmeans_instance.get_each_cluster_size()
        for i, v in enumerate(answer_each_size):
            eq_(v, actual_each_size[i])
        
        actual_assign = kmeans_instance.get_assign_list()
        matched_results = (answer == actual_assign)
        ok_(np.all(matched_results))

    # ステップごとの学習に成功すること
    def test_success_learning_step_by_step(self):
        kmeans_instance = KMeans()
        samples = self.create_test_mixture_random_samples(kmeans_instance.k)
        kmeans_instance.set_samples(samples)

        while not kmeans_instance.converged: 
            ok_(kmeans_instance.learn(steps = 1))
            print kmeans_instance.get_assign_list()
            print [c.centroid for c in kmeans_instance.get_clusters()]

    # 途中経過を確認できること
    def test_success_check_learning_process(self):
        kmeans_instance = KMeans()
        samples = self.create_test_mixture_random_samples(kmeans_instance.k)
        kmeans_instance.set_samples(samples)

        print 'process...'

        kmeans_instance.set_random_centroids()
        print kmeans_instance.get_assign_list()
        print [c.centroid for c in kmeans_instance.get_clusters()]

        while not kmeans_instance.converged: 
            ok_(kmeans_instance.learn(steps = 1))
            print kmeans_instance.get_assign_list()
            print [c.centroid for c in kmeans_instance.get_clusters()]

if __name__ == '__main__':
    unittest.main()


