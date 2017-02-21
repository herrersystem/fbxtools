#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import Fbx

## Initialize and connect app.
app = Fbx('http://192.168.0.254')
app.get_session_token()


from fbxtools.fbx import Fbx

@app.api.call('/api/v3/system/')
def get_system():
	'''
	GET /api/v3/system/
	''' 
	return {}

if __name__ == "__main__":
	resp = get_system()['data']
	if resp['success']:
		print (resp['result'])
	else:
		print (resp)
	
