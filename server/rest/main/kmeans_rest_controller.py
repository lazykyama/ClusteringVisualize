#!/usr/bin/env python
# -*- coding: utf-8 -*-

# インポート関連のおまじない
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../engine/main/common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../engine/main/kmeans'))

from kmeans import *

from rest_sub_controller import *

class KMeansRestController(RestSubController):

    def execute(self, query):
        return self.create_response(200, 'from KMeansRestController.')
