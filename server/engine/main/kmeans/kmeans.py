#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np

from operator import itemgetter

from cluster import Cluster

class KMeans:
    RANDOM_STATE = np.random.RandomState()
    PRECISION    = 8
        
    def __init__(self, k = 5): 
        self.k         = k
        self.converged = False
        self.started   = False

        self._samples  = None
        self._clusters = []
        for i in range(self.k):
            cluster = Cluster()
            self._clusters.append(cluster)

        self._centroids = []

    # 再初期化
    def _reinitialize(self):
        self.converged = False
        self.started   = False

    # 初期割り当て
    def set_init_assign(self, assigns = None):
        if assigns is None:
            raise TypeError(('set_init_assign() takes at least '
                             'a positional argument.'))

        # 入力されたアサインリストが妥当かチェックする
        if len(assigns) != len(self._samples):
            raise ValueError(('assign list is invalid length: '
                              'expected = ' + str(len(self._samples)) + ', '
                              'actual = ' + str(len(assigns)) + '.'))
        assign_min = np.min(assigns)
        assign_max = np.max(assigns)
        if assign_min < 0 or self.k <= assign_max:
            raise ValueError(('assign list has invalid value: '
                              'expected = (0,' + assign_max  + '), '
                              'actual = (' + assign_min +
                              ', ' + assign_max  + ').'))
        
        # 割り当てに応じてクラスタへのサンプル振り分けを実施
        KMeans._assign_cluster(self._clusters, self._samples, assigns)

        # 各クラスタのセントロイドを更新する
        self._centroids = [cluster.calc_centroid() 
                           for cluster in self._clusters]
        self.started = True
        
    # サンプルを受け取る
    def set_samples(self, samples = None):
        if samples is None:
            raise TypeError(('set_samples() takes at least '
                             'a positional argument.'))

        self._reinitialize()
        self._samples = np.array(samples)

    # セントロイドを受け取る
    # @notice set_samplesを呼び出す前に呼ばないこと！
    def set_centroids(self, centroids = None):
        if centroids is None:
            raise TypeError(('set_centroids() takes at least '
                             'a positional argument.'))
        
        self._reinitialize()
        for i, cluster in enumerate(self._clusters):
            cluster.set_centroid(np.array(centroids[i]))

        # 各クラスタのセントロイドを更新する
        self._centroids = [cluster.calc_centroid() 
                           for cluster in self._clusters]
        
        # ランダムな初期割り当てを抑制する
        self.started = True

    # 初期割り当てを実施
    # @notice set_samplesを呼んだ後に呼ぶこと！
    def set_random_centroids(self):
        # ランダムな割り当て
        if not self.started:
            KMeans.assign_random_cluster(self._clusters, self._samples)
            # 各クラスタのセントロイドを更新する
            self._centroids = [cluster.calc_centroid() 
                               for cluster in self._clusters]
            self.started = True
        
            
    # 持っているサンプルでk-means実行
    def learn(self, steps = None):
        if self.converged:
            # 既に収束している場合はFalseを返す
            return False

        # 初回はランダムなクラスタ割り当てを実施
        self.set_random_centroids()
                
        # 収束するまで繰り返す
        cnt = 0
        while not self.converged and (steps is None or cnt < steps):
            # 必要に応じて再割当てする
            self.converged = KMeans.reassign_by_centroid(
                self._centroids, self._clusters, self._samples)
            # 各クラスタのセントロイドを更新する
            self._centroids = [cluster.calc_centroid() 
                               for cluster in self._clusters]
            cnt += 1
            
        return True

    # ランダムなクラスタ割り当てリストを生成
    @staticmethod
    def generate_random_assigns(clusters_size = None, samples_size = None):
        if clusters_size is None or samples_size is None:
            raise TypeError(('generate_random_assign() takes at least '
                             '2 positional arguments.'))

        # ランダムなインデックスリストを生成
        # 実装の都合上、みんなだいたい同じように割り当てる
        if samples_size < clusters_size:
            raise TypeError(('#samples < #clusters is invalid.'))
        random_cluster_assigns = np.hstack((
                np.arange(clusters_size), 
                np.random.randint(0, clusters_size,
                                  samples_size - clusters_size)))
                                  # samples.shape[0] - clusters_size)))
        
        return random_cluster_assigns
    
    # ランダムなクラスタ割り当てを実施
    @staticmethod
    def assign_random_cluster(clusters = None, samples = None):
        if clusters is None or samples is None:
            raise TypeError(('assign_random_cluster() takes at least '
                             '2 positional arguments.'))

        clusters_size = len(clusters)
        samples_size  = len(samples)

        # 各クラスタに割り当てるサンプル数を決定
        # @todo とりあえず各クラスタに均等に割り当てる
        random_cluster_assigns = KMeans.generate_random_assigns(
            clusters_size, samples_size)
        
        # サンプルにクラスタを割り当てる
        KMeans._assign_cluster(clusters, samples, random_cluster_assigns)

    # サンプルにクラスタを割り当てる
    @staticmethod
    def _assign_cluster(clusters, samples, assigns):
        # クラスタIDに応じて、各クラスタにサンプルを渡す
        for i, cluster in enumerate(clusters):
            assigned_samples = [(j, samples[j]) for j, id
                                in enumerate(assigns)
                                if i == id]
            cluster.initialize(assigned_samples)

    # 現時点のクラスタ割り当てリストを返す
    @staticmethod
    def _tolist_current_assign(clusters, samples):
        clusters_size = len(clusters)
        curr_assigned = [clusters_size for v in samples]
        for i, cluster in enumerate(clusters):
            if cluster.sample_indexes is None:
                continue
            
            for idx in cluster.sample_indexes:
                curr_assigned[idx] = i

        return curr_assigned

    # 与えられたセントロイドベースで再割当てする
    @staticmethod
    def reassign_by_centroid(centroids = None, 
                             clusters = None, samples = None):
        if centroids is None or clusters is None or samples is None:
            raise TypeError(('assign_random_cluster() takes at least '
                             '3 positional arguments.'))

        centroids_size = len(centroids)
        clusters_size  = len(clusters)
        samples_size   = len(samples)

        # 今の割り当てを保持しておく
        curr_assigned = KMeans._tolist_current_assign(clusters, samples)

        # 新しい割り当てを作成する。
        # 同程度の距離にあるクラスタが複数の場合は、
        # 決定境界面にサンプルが存在しているため、どちらでもよい気がする。
        # しいて決めるならクラス内分散が多い方に割り当てるべき？
        # @todo 現状、centroidsにnanが含まれるとエラーになる
        updated_assign = [np.argmin(np.sum(np.power(sample - centroids, 2),
                                        axis = 1))
                       for sample in samples]

        # 新しい割り当てと古い割り当てに差分があるかチェックする
        # @todo この書き方だと最適化が効きにくいかも。。。
        is_updated = True
        if np.all(updated_assign == curr_assigned):
            is_updated = False

        # 差分がなければ収束しているのでTrueで戻る
        if not is_updated:
            return True

        # 差分がある場合は割り当て直して戻る
        KMeans._assign_cluster(clusters, samples, updated_assign)
        return False

    # 呼び出された瞬間の内部状態を返す
    def get_clusters(self):
        return [cluster for cluster in self._clusters]

    # 呼び出された瞬間のセントロイドを返す
    def get_centroids(self):
        return self._centroids

    # クラスタへの割り当てリストを返す
    def get_assign_list(self):
        return KMeans._tolist_current_assign(self._clusters, self._samples)

    # 各クラスタに属しているサンプル数を返す
    def get_each_cluster_size(self):
        return [len(cluster.sample_indexes) for cluster in self._clusters]

    # 全体のサンプル数を返す
    def get_samples_size(self):
        return len(self._samples)

    # サンプルを返す
    def get_samples(self):
        return self._samples

    # サンプルをリストとして返す
    def get_samples_as_list(self):
        return self._samples.tolist()
