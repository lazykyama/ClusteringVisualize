#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import mimetypes

import os

from rest_controller import *
from http_response_wrapper import *

# from http://ja.pymotw.com/2/BaseHTTPServer/index.html
class VisualizeServer(BaseHTTPRequestHandler):

    CONTENTS_ROOT_PATH = '../../contents/'
    FAVICON_PATH = CONTENTS_ROOT_PATH + 'favicon.ico'
    
    DEFAULT_PORT = 8280

    def do_GET(self):
        # リクエストをパース
        parsed_path = urlparse.urlparse(self.path)
        """
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        print 'info: '
        print message
        """

        # dispatch.
        # パフォーマンスを気にする場合は、self.wfileを渡して、ストリーム処理させるべき？
        parsed_query_list = [qc.split('=') for qc in parsed_path.query.split('&')
                             if qc.find('=') != -1]
        parsed_query = dict(parsed_query_list)
        response = (self.dispatch_request(parsed_path.path))(
            parsed_path.path, parsed_query)
        
        # construct response.
        self.send_response(response[HttpResponseWrapper.KEY_RESPONSE_SC])
        self.send_header('Content-Type',
                         response[HttpResponseWrapper.KEY_RESPONSE_MIME])
        self.end_headers()
        self.wfile.write(response[HttpResponseWrapper.KEY_RESPONSE_BODY])
        
        return

    # リクエストされたパスに応じて必要な関数を返す
    def dispatch_request(self, requested_path):
        if requested_path.startswith('/contents/'):
            return self.return_contents
        elif requested_path.startswith('/rest/'):
            return self.execute_rest_request
        elif requested_path.startswith('/favicon.ico'):
            return self.return_favicon
        else:
            return HttpResponseWrapper.return_not_found

    # 指定パスのコンテンツを返す
    def return_contents(self, requested_path, requested_query):
        # 指定された名前のコンテンツを返す
        contents_name = requested_path.split('/contents/')[1]
        
        # ルートを指定された場合はindex.htmlを返すように設定
        if len(contents_name) == 0:
            contents_name = 'index.html'
        
        # 指定された名前のコンテンツが上位ディレクトリを見ていないかチェック
        abs_contents_root = os.path.abspath(
            VisualizeServer.CONTENTS_ROOT_PATH)
        abs_user_path = os.path.abspath(
            VisualizeServer.CONTENTS_ROOT_PATH + contents_name)

        response = HttpResponseWrapper.create_empty_response()
        if not abs_user_path.startswith(abs_contents_root):
            # 上位ディレクトリを見ようとしているためNG
            response = HttpResponseWrapper.create_bad_request_response()

        elif os.path.exists(abs_user_path):
            # 上位ディレクトリを見ようとしておらず、かつ指定ファイルが存在
            response[HttpResponseWrapper.KEY_RESPONSE_BODY] = self.load_file(
                abs_user_path)
            mime_type, encoding = mimetypes.guess_type(abs_user_path)

            if mime_type is None:
                response[HttpResponseWrapper.KEY_RESPONSE_MIME] = 'unknown/unknown'
            else:
                response[HttpResponseWrapper.KEY_RESPONSE_MIME] = mime_type

        else:
            # 上位ディレクトリを見ていないが、指定ファイルがない
            response = HttpResponseWrapper.return_not_found(requested_path,
                                                            requested_query)
            
        return response

    # RESTリクエストを処理する
    # 具体的な処理は専用コントローラに委譲
    def execute_rest_request(self, requested_path, requested_query):
        # execute.
        controller = RestController()
        response = controller.execute_with_subcontroller(
            requested_path.split('rest/')[1], requested_query)
        return response

    # faviconがあれば返す
    def return_favicon(self, requested_path, requested_query):
        response = HttpResponseWrapper.create_empty_response()
        if os.path.exists(VisualizeServer.FAVICON_PATH):
            # @todo キャッシュしておく？
            response[HttpResponseWrapper.KEY_RESPONSE_BODY] = self.load_file(
                VisualizeServer.FAVICON_PATH)
            response[HttpResponseWrapper.KEY_RESPONSE_MIME] = 'image/vnd.microsoft.icon'
        else: 
            response = HttpResponseWrapper.return_not_found(
                requested_path, requested_query)

        return response

    # 指定パスのファイルからテキストで読み込んでくる
    def load_file(self, abs_file_path):
        message = ''
        for line in open(abs_file_path, 'r'):
            message += line
        return message
        

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', VisualizeServer.DEFAULT_PORT),
                        VisualizeServer)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
