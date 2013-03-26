#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RestSubController:
    def execute(self, query):
        raise NotImplementedError('Not override...')

    def create_response(self, sc, body):
        return {'sc': sc, 'body': body}
