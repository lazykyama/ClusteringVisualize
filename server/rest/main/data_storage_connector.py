#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dummy_storage import *

class DataStorageConnector:

    TYPE_DUMMY_STORAGE = 'dummy'

    @staticmethod
    def connect():
        # @todo 設定ファイルとかで切り替えたい
        storage_type = DataStorageConnector.TYPE_DUMMY_STORAGE
        
        if storage_type == DataStorageConnector.TYPE_DUMMY_STORAGE:
            return DummyStorage()
        else:
            raise TypeError('Unknown storage type: ' + storage_type)
