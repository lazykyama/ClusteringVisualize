#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インポート関連のおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) +
                                '/../../engine/main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + 
                                '/../../engine/main/kmeans'))

import json
import uuid

from kmeans import *
from data_generator import *

from rest_sub_controller import *
from data_storage_connector import * 
from base_storage import *

# データアクセス用クラス
class KMeansDataAccessor:
    _KEY_PARAM_K = 'k'
    _KEY_SAMPLES = 'samples'
    _KEY_ASSIGNS = 'assigns'
    
    @staticmethod
    def exists_session(storage, session_id):
        return storage.exists_value(session_id)

    @staticmethod
    def store_session(storage, session_id, kmeans_instance):
        # 必要な値をjsonに変換し、実際のアクセッサに渡す
        # 格納対象は、k, samples, assignments
        kmeans_json_dict = {}
        kmeans_json_dict[KMeansDataAccessor._KEY_PARAM_K] = kmeans_instance.k
        samples = kmeans_instance.get_samples()
        kmeans_json_dict[KMeansDataAccessor._KEY_SAMPLES] = samples.tolist()
        kmeans_json_dict[KMeansDataAccessor._KEY_ASSIGNS] = kmeans_instance.get_assign_list()
        
        kmeans_json = json.dumps(kmeans_json_dict)

        # jsonをセット
        storage.set_value(session_id, kmeans_json)
        return 

    @staticmethod
    def load_session(storage, session_id):
        # jsonの値を取ってきてkmeansのインスタンスにして返す
        kmeans_json = storage.get_value(session_id)

        kmeans_json_dict = json.loads(kmeans_json)

        # kmeansインスタンスをjsonから生成
        kmeans_inst = KMeans(
            k = kmeans_json_dict[KMeansDataAccessor._KEY_PARAM_K])
        kmeans_inst.set_samples(
            kmeans_json_dict[KMeansDataAccessor._KEY_SAMPLES])
        kmeans_inst.set_init_assign(
            kmeans_json_dict[KMeansDataAccessor._KEY_ASSIGNS])
        
        return kmeans_inst

class KMeansRestController(RestSubController):

    # 3次元データを仮定
    DEFAULT_SCALE = 5.0
    DEFAULT_MEAN = np.array([0, 0, 0])
    DEFAULT_COV  = DEFAULT_SCALE * np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]])

    # クエリのキー文字列
    KEY_SESSION_ID = 'sessionid'
    KEY_STEP       = 'step'
    KEY_SIZE       = 'size'
    KEY_K          = 'k'

    # レスポンスのキー文字列
    KEY_RESPONSE_SESSION_ID = 'sessionId'
    KEY_RESPONSE_RESULT_PAIRS = 'resultPairs'

    def __init__(self):
        self._storage = DataStorageConnector.connect()
        self._rand_data_gen = RandDataGenerator(dim = 3)

    @staticmethod
    def _validate_queries(query):
        # 必須パラメータの存在チェック
        if not query.has_key(KMeansRestController.KEY_SIZE):
            return False
        if not query.has_key(KMeansRestController.KEY_K):
            return False

        # 任意パラメータ含め内容チェック
        try:
            tmp_k = int(query[KMeansRestController.KEY_K], 10)
            tmp_size = int(query[KMeansRestController.KEY_SIZE], 10)
            
            if tmp_k <= 0 or tmp_size <= 0 or tmp_size < tmp_k:
                # サンプル数がクラスタ数を下回ると初期割り当てがおかしくなるのでNG
                return False

            if not query.has_key(KMeansRestController.KEY_STEP):
                # stepパラメータは任意なので、なければバリデート通過
                return True

            tmp_step = int(query[KMeansRestController.KEY_STEP], 10)
            if tmp_step <= 0:
                return False
        except: 
            return False
        return True

    @staticmethod
    def _convert_instance_to_response_message(session_id, kmeans_inst):
        response_dict = {}
        # セッションIDだけ先に追加しておく
        response_dict[KMeansRestController.KEY_RESPONSE_SESSION_ID] = session_id

        # サンプルと割り当ての組を作成し、リストに追加
        # 面倒なので両者のサイズは一致していると仮定
        result_list = []
        samples = kmeans_inst.get_samples()
        assigns = kmeans_inst.get_assign_list()
        samples_len = len(samples)
        for i in range(0, samples_len):
            a = assigns[i]
            s = samples[i].tolist()
            result_list.append((a, s))

        # 結果リストを変換元オブジェクトに追加
        response_dict[KMeansRestController.KEY_RESPONSE_RESULT_PAIRS] = result_list

        # json化して返す
        response_json = json.dumps(response_dict)
        return response_json

    def execute(self, query):
        # クエリのバリデート
        if not KMeansRestController._validate_queries(query):
            response = self.create_bad_req_response()
            return response
        
        # セッションIDが既知でない場合は、新規データセットを生成し、
        # 内部状態を変更してから、整形したレスポンスを返す
        size = int(query[KMeansRestController.KEY_SIZE], 10)
        param_k = int(query[KMeansRestController.KEY_K], 10)
        
        session_id = None
        if query.has_key(KMeansRestController.KEY_SESSION_ID):
            session_id = query[KMeansRestController.KEY_SESSION_ID]
        step = None
        if query.has_key(KMeansRestController.KEY_STEP):
            step = int(query[KMeansRestController.KEY_STEP], 10)

        if session_id is None or KMeansDataAccessor.exists_session(
            self._storage, session_id):
            # セッションを新規作成する場合
            # セッションIDを払い出す
            session_id = uuid.uuid4().hex
            
            # データ生成
            samples = self._rand_data_gen.generate_multivariate_norm(
                KMeansRestController.DEFAULT_MEAN,
                KMeansRestController.DEFAULT_COV,
                size)
            
            # kmeansの初期化
            kmeans_inst = KMeans(k = param_k)
            kmeans_inst.set_samples(samples)
            kmeans_inst.set_random_centroids()
            
            # レスポンス生成
            message = KMeansRestController._convert_instance_to_response_message(
                session_id, kmeans_inst)
            response = self.create_success_response(message)

            # 内部に保持
            # レスポンス生成後に格納するのは、ロールバックのため
            KMeansDataAccessor.store_session(self._storage,
                                             session_id, kmeans_inst)
            
            # 返す
            return response

        # セッションIDが既知の場合は、内部状態を取得する
        # ここは場合により、memcachedなどを利用する
        kmeans_inst = KMeansDataAccessor.load_session(self._storage, session_id)

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
        message = KMeansRestController._convert_instance_to_response_message(
            session_id, kmeans_inst)
        response = self.create_success_response(message)

        # 内部状態を変更
        KMeansDataAccessor.store_session(self._storage, 
                                         session_id, kmeans_inst)
            
        return response
