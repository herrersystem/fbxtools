#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/lcd/
'''
import requests
import json


def get_config(app):
	'''
	GET /api/v3/lcd/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}lcd/config/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			config=response['result']
		except KeyError:
			config=None
	
	return config


def update_config(app, config):
	'''
	PUT /api/v3/lcd/config/
	
	dict() config (example):
	{	
		"brightness": 50,
		"orientation": 90,
		"orientation_forced": false
    }
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]')
		return False
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}lcd/config/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			update=response['result']
		except KeyError:
			update=None
	
	return update
	
