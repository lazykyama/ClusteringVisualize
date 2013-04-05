#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インポートに絡むおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../main/'))

from dummy_storage import *

import unittest
from nose.tools import *

class TestDummyStorage(unittest.TestCase):
    
    def test_success_set_and_get_pair(self):
        dum_storage = DummyStorage()
        key = 'hogehoge'
        value = '{"key": "value1", "key2": "value2"}'

        dum_storage.set_value(key, value)
        reget_value = dum_storage.get_value(key)

        eq_(value, reget_value)

    def test_success_check_exists_value(self):
        dum_storage = DummyStorage()
        key = 'hogehoge'
        value = '{"key": "value1", "key2": {"inkey1" : "value21", "inkey2" : "value22"}}'

        dum_storage.set_value(key, value)
        ok_(dum_storage.exists_value(key))
