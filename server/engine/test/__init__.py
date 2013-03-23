#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, glob
from unittest import TestSuite, TestLoader, TextTestRunner

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_all_test_mods():
	'''同階層のテストを全部インポートする'''
	test_mods = []
	pwd = os.getcwd()
	os.chdir(CURRENT_DIR)
	try:
		for file in glob.glob('test*.py'):
			test_mods.append(__import__(os.path.splitext(file.split('/')[-1])[0], globals(), locals(), []))
		return test_mods
	finally:
		os.chdir(pwd)

def get_all_test_pkgs():
	'''テストが定義されたパッケージをインポートする'''
	test_pkgs = []
	pwd = os.getcwd()
	os.chdir(CURRENT_DIR)
	try:
		for file in glob.glob('*/__init__.py'):
			pkg = __import__(file.split('/')[0], globals(), locals(), [])
			if getattr(pkg, 'get_all_test_suite', None):
				test_pkgs.append(pkg)
		return test_pkgs
	finally:
		os.chdir(pwd)

def get_all_test_suite():
	'''すべてのテストが含まれたTestSuiteを返す'''
	all_tests = TestSuite()

	for tm in get_all_test_mods():
		suite = TestLoader().loadTestsFromModule(tm)
		all_tests.addTest(suite)

	for tp in get_all_test_pkgs():
		suite = tp.get_all_test_suite()
		all_tests.addTest(suite)

	return all_tests

if __name__ == "__main__":
	ttr = TextTestRunner(verbosity = 2)
	ttr.run(get_all_test_suite())
