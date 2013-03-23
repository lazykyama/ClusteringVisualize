#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インクルードに絡むおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../main/kmeans'))

import unittest
from nose.tools import *

import data_generator
import kmeans

class TestKMeans(unittest.TestCase):

    def test_initialize(self):
        ok_(True)

    def test_success_learning_completely(self):
        ok_(True)

    def test_success_learning_step_by_step(self):
        ok_(True)

    def test_change_status_by_different_k(self):
        ok_(True)

    def test_success_reloading_samples(self):
        ok_(True)

if __name__ == '__main__':
    unittest.main()


