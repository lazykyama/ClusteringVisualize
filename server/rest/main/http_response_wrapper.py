#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib

class HttpResponseWrapper:
    KEY_RESPONSE_SC = 'sc'
    KEY_RESPONSE_BODY = 'body'

    # 不許可リクエストなどには404を返す
    @staticmethod
    def return_not_found(requested_path, requested_query):
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.NOT_FOUND,
                HttpResponseWrapper.KEY_RESPONSE_BODY: ('%s is not found.'
                                                    % requested_path)}
    @staticmethod
    def create_empty_response():
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.OK,
                HttpResponseWrapper.KEY_RESPONSE_BODY: ''}

