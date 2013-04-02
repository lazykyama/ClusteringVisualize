#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インポート関連のおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../engine/main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../engine/main/kmeans'))

from kmeans import *
from data_generator import *

from rest_sub_controller import *
from data_storage_connect import * 
from base_storage import *

class KMeansDataAccessor:
    @staticmethod
    def exists_session(session_id):
        return True

    @staticmethod
    def store_session(session_id, kmeans_instance):
        pass

    @staticmethod
    def load_session(session_id):
        return None

class KMeansRestController(RestSubController):

    # 3次元データを仮定
    DEFAULT_SCALE = 5.0
    DEFAULT_MEAN = np.array([0, 0, 0])
    DEFAULT_COV  = DEFAULT_SCALE * np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]])

    def __init__(self):
        self._storage = DataStorageConnector.connect()
        self._rand_data_gen = RandomDataGenerator()

    @staticmethod
    def _validate_queries(query):
        return True

    @staticmethod
    def _convert_instance_to_response_message(session_id, kmeans_inst):
        pass

    def execute(self, query):

        # クエリのバリデート
        if not KMeansRestController._validate_queries(query):
            response = self.create_bad_req_response()
            return response

        # セッションIDが既知でない場合は、新規データセットを生成し、
        # 内部状態を変更してから、整形したレスポンスを返す
        session_id = None
        if query.has_key(''):
            session_id = query['']
        size = None
        if query.has_key(''):
           size = query['']
        param_k = None
        if query.has_key(''):
            param_k = query['']
        step = None
        if query.has_key(''):
            step = query['']
        
        if KMeansDataAccessor.exists_session(session_id):
            # データ生成
            samples = self._rand_data_gen.generate_multivariate_norm(
                KMeansRestController.DEFAULT_MEAN,
                KMeansRestController.DEFAULT_COV,
                size)
            
            # kmeansの初期化
            kmeans_inst = KMeans(k = param_k)
            kmeans_inst.set_samples(samples)
            
            # レスポンス生成
            response = KMeansRestController._convert_instance_to_response_message(
                session_id, kmeans_inst)

            # 内部に保持
            # レスポンス生成後に格納するのは、ロールバックのため
            KMeansDataAccessor.store_session(session_id, kmeans_inst)
            
            # 返す
            return response

        # セッションIDが既知の場合は、内部状態を取得する
        # ここは場合により、memcachedなどを利用する
        kmeans_inst = KMeansDataAccessor.load_session(session_id)

        # サンプルサイズが変更された場合は、指定サイズのデータセットを新規作成する
        # 変更がなければ何もしない
        if size != kmeans_inst.get_samples_size():
            # サンプルを再作成し、置き換える
            new_samples = self._rand_data_gen.generate_multivariate_norm(
                KMeansRestController.DEFAULT_MEAN,
                KMeansRestController.DEFAULT_COV,
                size)
            kmeans_inst.set_samples(new_samples)
            kmeans_inst.set_random_centroids()

        # 同様に、クラスタ数が変更された場合は、初期の割り当てをやり直す
        # クラスタ数に変更がなければ何もしない
        if param_k != kmeans_inst.k:
            # 初期割り当てからやり直す
            samples = kmeans_inst.get_samples()
            kmeans_inst = KMeans(k = param_k)
            kmeans_inst.set_samples(samples)
            kmeans_inst.set_random_centroids()
            
        # ステップ数に応じて、k-meansの学習を実行
        if step is not None:
            kmeans_inst.learn(steps = step)
        else:
            # 収束するまで学習させるので引数なし
            kmeans_inst.learn()

        # 学習結果をレスポンスとして整形
        response = self.create_success_response(kmeans_inst.to_json())

        # 内部状態を変更
        KMeansDataAccessor.store_session(session_id, kmeans_inst)
            
        return response
