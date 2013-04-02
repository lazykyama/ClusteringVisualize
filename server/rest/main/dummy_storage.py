#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_storage import *

class DummyStorage(BaseStorage):

    def close(self): 
        raise NotImplementedError('Not override...')

    def get_value(self, key = None):
        raise NotImplementedError('Not override...')

    def set_value(self, key = None, value = None, expire = 0):
        raise NotImplementedError('Not override...')

    def exists_value(self, key = None):
        raise NotImplementedError('Not override...')
