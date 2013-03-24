#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import uuid

class Cluster:
    def __init__(self):
        self.id = uuid.uuid4()

        self.centroid       = None
        self.sample_indexes = None

        self._samples       = None

    # サンプルでクラスタを初期化
    def initialize(self, samples = None):
        if samples is None:
            raise TypeError(('initialize() takes at least '
                             'a positional argument.'))

        self.sample_indexes  = [s[0] for s in samples]
        self._samples        = np.array([s[1] for s in samples])

        if len(samples) != 0:
            # サンプルが空でないときのみセントロイドをクリア
            self.centroid = None
        
    # セントロイドをセット
    def set_centroid(self, centroid = None):
        if centroid is None:
            raise TypeError(('set_centroid() takes at least '
                             'a positional argument.'))
        self.centroid = centroid
        
    # セントロイドを計算
    def calc_centroid(self):
        if self.centroid is None:
            # 普通に算術平均出すのみ
            self.centroid = np.mean(self._samples, axis = 0)

        return self.centroid
