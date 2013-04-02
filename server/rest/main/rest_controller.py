#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kmeans_rest_controller import *
from http_response_wrapper import *

import httplib

class RestController:
    # コマンドとクエリをサブコントローラに渡して実行させる
    def execute_with_subcontroller(self, command, query):
        # 本当はこのへんでメッセージキューを利用したほうがいいと思いますが、
        # 簡易実装ということでひとつ。。。
        response = ''
        try:
            subcontroller = RestSubControllerFactory.create_subcontroller(command)
            response = subcontroller.execute(query)
        except:
            # 例外発生時は500エラー
            response = HttpResponseWrapper.create_internal_server_error()
        finally: 
            return response

class RestSubControllerFactory:
    
    @staticmethod
    def create_subcontroller(command):
        if command == 'kmeans_results':
            return KMeansRestController()
        else:
            raise TypeError('Unknown command: ' + command)
