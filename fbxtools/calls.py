#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/call/
'''
import requests
import time


def get_call_log(app, _datetime=time.time()):
	'''
	GET /api/v3/call/log/
	'''
	call_log=False
	
	if not app.AUTH_CALLS:
		print('[fbx-tools] > Not Allowed [CALLS]')
		return -1
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}call/log/'.format(
			app.api_base_url
		), 
		params={'_dc': _datetime},
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			call_log=response['result']
		except KeyError:
			call_log=None
	
	return call_log


def delete_call(app, _id):
	'''
	DELETE /api/v3/call/log/{id}
	'''
	deletion=False
	
	if not app.AUTH_CALLS:
		print('[fbx-tools] > Not Allowed [CALLS]')
		return -1
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}call/log/{}'.format(
			app.api_base_url, 
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		deletion=True
	
	return deletion
