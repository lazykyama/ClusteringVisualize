#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kmeans_rest_controller import *
from http_responose_wrapper import *

import httplib

class RestController:
    # コマンドとクエリをサブコントローラに渡して実行させる
    def execute_with_subcontroller(self, command, query):
        # 本当はこのへんでメッセージキューを利用したほうがいいと思いますが、
        # 簡易実装ということでひとつ。。。
        try:
            subcontroller = RestSubControllerFactory.create_subcontroller(command)
        except:
            # 例外発生時は500エラー
            err_response = HttpResponseWrapper.create_empty_response()
            err_response[HttpResponseWrapper.KEY_RESPONSE_SC] = httplib.INTERNAL_SERVER_ERROR
            err_response[HttpResponseWrapper.KEY_RESPONSE_BODY] = httplib.response[
                httplib.INTERNAL_SERVER_ERROR]
            return err_response
        
        response = subcontroller.execute(query)
        return response

class RestSubControllerFactory:
    
    @staticmethod
    def create_subcontroller(command):
        if command == 'kmeans_results':
            return KMeansRestController()
        else:
            raise TypeError('Unknown command: ' + command)
