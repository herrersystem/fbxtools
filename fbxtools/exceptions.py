#!/usr/bin/env python

class FbxSessionToken(Exception):
	def __init__(self, err_code, err_msg):
		Exception.__init__(self, '[%s] %s' % (err_code, err_msg))


class FbxAppToken(Exception):
	def __init__(self, err_code, err_msg):
		Exception.__init__(self, '[%s] %s' % (err_code, err_msg))
