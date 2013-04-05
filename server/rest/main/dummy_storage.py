#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_storage import *

import time

# ダミーのストレージアクセスクラス
# 実際にはオンメモリのキーバリューを利用する
class DummyStorage(BaseStorage):

    EMULATED_STORAGE = {}
    CORRESPONDIN_EXPIRE = {}

    def open(self, path):
        # 本来はここでopenしたりするんでしょうが、何もしないです
        pass

    def close(self): 
        # 本来はここでcloseしたりするんでしょうが（ｒｙ
        pass

    def get_value(self, key = None):
        if key is None:
            raise TypeError('get_value() takes at least an argument.')

        expire_in_sec = DummyStorage.CORRESPONDIN_EXPIRE[key]
        now_time_in_sec = round(time.time())
        if expire_in_sec > 0 and expire_in_sec < now_time_in_sec:
            # 現在時刻以前にexpireしていると思われるデータは捨てる
            return None
        
        return DummyStorage.EMULATED_STORAGE[key]

    def set_value(self, key = None, value = None, expire_in_sec = 0):
        if key is None or value is None:
            raise TypeError('set_value() takes at least two argument.')
        if expire_in_sec < 0:
            raise ValueError(('the negative expire value[' 
                              + expire_in_sec + '] is denied.'))

        now_time_in_sec = round(time.time())
        expire_unix_in_sec = 0
        if expire_in_sec != 0:
            # expire = 0の時はそのまま格納する
            expire_unix_in_sec = now_time_in_sec + expire_in_sec
        DummyStorage.CORRESPONDIN_EXPIRE[key] = expire_unix_in_sec
        
        DummyStorage.EMULATED_STORAGE[key] = value

        return 

    def exists_value(self, key = None):
        if key is None:
            raise TypeError('get_value() takes at least an argument.')

        return DummyStorage.EMULATED_STORAGE.has_key(key)
