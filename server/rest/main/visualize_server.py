#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse

import os

from rest_controller import *

# from http://ja.pymotw.com/2/BaseHTTPServer/index.html
class VisualizeServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
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

        # dispatch.
        sc = 200
        contents_root_path = '../../contents/'
        if parsed_path.path.startswith('/contents/'):
            # 指定された名前のコンテンツを返す
            contents_name = parsed_path.path.split('/contents/')[1]

            # ルートを指定された場合はindex.htmlを返すように設定
            if len(contents_name) == 0:
                contents_name = 'index.html'
                    
            # 指定された名前のコンテンツが上位ディレクトリを見ていないかチェック
            abs_contents_root = os.path.abspath(contents_root_path)
            abs_user_path = os.path.abspath(contents_root_path + contents_name)

            if not abs_user_path.startswith(abs_contents_root):
                # 上位ディレクトリを見ようとしているためNG
                sc = 400
                message = 'Bad Request.\r\n' + message

            elif os.path.exists(abs_user_path):
                # 上位ディレクトリを見ようとしておらず、かつ指定ファイルが存在
                message = self.load_file(contents_root_path + contents_name)
            else:
                # 上位ディレクトリを見ていないが、指定ファイルがない
                sc = 404
                message = 'File is not found.\r\n' + message
                
        elif parsed_path.path.startswith('/rest'):
            # execute.
            controller = RestController()
            response = controller.execute_with_subcontroller(
                parsed_path.path.split('rest/')[1],
                parsed_path.query)
            print response
        elif parsed_path.path.startswith('/favicon.ico'):
            # contentsあたりにfaviconがあれば返す
            if os.path.exists(contents_root_path + 'favicon.ico'):
                message = self.load_file(contents_root_path + 'favicon.ico')
            else: 
                sc = 404
                message = 'File is not found.\r\n' + message
        else:
            # 許可していないリクエストはとりあえず404にしておく
            # RFC的にもOKっぽいので
            sc = 404

        # construct response.
        self.send_response(sc)
        self.end_headers()
        self.wfile.write(message)
        
        return

    # 指定パスのファイルからテキストで読み込んでくる
    def load_file(self, abs_file_path):
        message = ''
        for line in open(abs_file_path, 'r'):
            message += line
        return message
        

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8280), VisualizeServer)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
