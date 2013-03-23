#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class KMeans:

    def __init__(self, k = 5): 
        self.k = k
        self.converged = False
        self.samples = None

    # データ集合を受け取る
    def load_samples(self, samples = None):
        raise TypeError('This method is not supported, yet.')

    # データ集合を更新する
    def reload_samples(self, samples = None):
        raise TypeError('This method is not supported, yet.')

    # 持っているデータでk-means実行
    def learn(self, steps = None): 
        raise TypeError('This method is not supported, yet.')

    # 収束しているかを返す
    def converges_learning(self):
        return self.converged

    # 呼び出された瞬間の内部状態を返す
    def get_clusters(self):
        raise TypeError('This method is not supported, yet.')
