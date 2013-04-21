#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback

from kmeans_rest_controller import *
from http_response_wrapper import *

class RestController:
    # コマンドとクエリをサブコントローラに渡して実行させる
    def execute_with_subcontroller(self, command, query):
        # 本当はこのへんでメッセージキューを利用したほうがいいと思いますが、
        # 簡易実装ということでひとつ。。。
        response = ''
        try:
            subcontroller = RestSubControllerFactory.create_subcontroller(command)
            response = subcontroller.execute(query)
        except Exception, detail:
            # http://melpystudio.blog82.fc2.com/blog-entry-87.htmlから
            # エラーの情報をsysモジュールから取得
            info = sys.exc_info()
            # tracebackモジュールのformat_tbメソッドで特定の書式に変換
            tbinfo = traceback.format_tb(info[2])
            # 収集した情報を読みやすいように整形して出力する
            error_msg_header = 'internal server error:'
            DELIMITER_LENGTH = 40
            print error_msg_header.ljust(DELIMITER_LENGTH, '=')
            for tbi in tbinfo:
                print tbi
            print '  %s' % str(info[1])
            print '\n'.rjust(DELIMITER_LENGTH, '=')

            # 例外発生時は500エラー
            response = HttpResponseWrapper.create_internal_server_error()
        finally: 
            return response

class RestSubControllerFactory:
    
    @staticmethod
    def create_subcontroller(command):
        if command == 'kmeans_result':
            return KMeansRestController()
        else:
            raise TypeError('Unknown command: ' + command)
