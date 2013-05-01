#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib

class HttpResponseWrapper:
    KEY_RESPONSE_SC = 'sc'
    KEY_RESPONSE_BODY = 'body'
    KEY_RESPONSE_MIME = 'mime'

    # 不許可リクエストなどには404を返す
    @staticmethod
    def return_not_found(requested_path, requested_query):
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.NOT_FOUND,
                HttpResponseWrapper.KEY_RESPONSE_BODY: ('%s is not found.'
                                                    % requested_path),
                HttpResponseWrapper.KEY_RESPONSE_MIME: 'text/plain'}
    @staticmethod
    def create_bad_request_response():
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.BAD_REQUEST,
                HttpResponseWrapper.KEY_RESPONSE_BODY: httplib.responses[httplib.BAD_REQUEST],
                HttpResponseWrapper.KEY_RESPONSE_MIME: 'text/plain'}

    @staticmethod
    def create_internal_server_error():
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.INTERNAL_SERVER_ERROR,
                HttpResponseWrapper.KEY_RESPONSE_BODY: httplib.responses[httplib.INTERNAL_SERVER_ERROR],
                HttpResponseWrapper.KEY_RESPONSE_MIME: 'text/plain'}

    @staticmethod
    def create_empty_response():
        return {HttpResponseWrapper.KEY_RESPONSE_SC: httplib.OK,
                HttpResponseWrapper.KEY_RESPONSE_BODY: '',
                HttpResponseWrapper.KEY_RESPONSE_MIME: 'text/plain'}

