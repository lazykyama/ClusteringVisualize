#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kmeans_rest_controller import *

class RestController:
    # コマンドとクエリをサブコントローラに渡して実行させる
    def execute_with_subcontroller(self, command, query):
        # 本当はこのへんでメッセージキューを利用したほうがいいと思いますが、
        # 簡易実装ということでひとつ。。。
        try:
            subcontroller = RestSubControllerFactory.create_subcontroller(command)
        except:
            # @todo 例外処理＆戻り値の設計
            return None
        
        response = subcontroller.execute(query)
        return response

class RestSubControllerFactory:
    
    @staticmethod
    def create_subcontroller(command):
        if command == 'kmeans_results':
            return KMeansRestController()
        else:
            raise TypeError('Unknown command: ' + command)
