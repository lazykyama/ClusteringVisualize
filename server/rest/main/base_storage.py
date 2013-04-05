#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ストレージアクセス用クラスの基底クラス
# どちらかというとinterface的位置づけ
class BaseStorage:
    def open(self, path):
        raise NotImplementedError('Not overrided...')
    
    def close(self): 
        raise NotImplementedError('Not overrided...')

    def get_value(self, key = None):
        raise NotImplementedError('Not overrided...')

    def set_value(self, key = None, value = None, expire_in_sec = 0):
        raise NotImplementedError('Not overrided...')

    def exists_value(self, key = None):
        raise NotImplementedError('Not overrided...')
