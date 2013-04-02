#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http_response_wrapper import *

class RestSubController:
    def execute(self, query):
        raise NotImplementedError('Not override...')

    def create_success_response(self, body):
        response =  HttpResponseWrapper.create_empty_response()
        response[HttpResponseWrapper.KEY_RESPONSE_BODY] = body
        return response

    def create_bad_req_response(self):
        response =  HttpResponseWrapper.create_bad_request_response()
        return response
