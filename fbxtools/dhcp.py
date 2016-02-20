#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/connection/
'''
import requests
import json


def get_config(app):
	'''
	GET /api/v3/dhcp/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}dhcp/config/'.format(
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
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return config


def update_config(app, config):
	'''
	PUT /api/v3/dhcp/config/
	
	dict() config (example):
	{
		"enabled": True,
		"ip_range_start": "192.168.1.10",
		"ip_range_end": "192.168.1.80",
		"sticky_assign": False",
		"dns": ['8.8.8.8', '8.8.4.4']
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}dhcp/config/'.format(
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
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return update
	

def get_static_lease(app, _id=''):
	'''
	GET /api/v3/dhcp/static_lease/{id}
	'''
	static_lease=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}dhcp/static_lease/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			static_lease=response['result']
		except KeyError:
			static_lease=None
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return static_lease
	

def update_static_lease(app, config, _id):
	'''
	PUT /api/v3/dhcp/static_lease/{id}
	
	dict() config (example):
	{
	  "comment": "raspberrypi (FTP server)",
	  "ip": "192.168.1.42"
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}dhcp/static_lease/{}'.format(
			app.api_base_url,
			_id
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
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return update


def create_static_lease(app, config):
	'''
	POST /api/v3/dhcp/static_lease/
	
	dict() config (example):
	{
		"ip": "192.168.1.42",
		"mac": "00:11:22:33:44:55",
		"comment": "raspberrypi (HTTP server)"
	}
	'''
	static_lease=False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}dhcp/static_lease/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			static_lease=response['result']
		except KeyError:
			static_lease=None
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return static_lease


def delete_static_lease(app, _id):
	'''
	DELETE /api/v3/dhcp/static_lease/{id}
	'''
	delete=False
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}dhcp/static_lease/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		delete=True
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return delete


def get_dynamic_lease(app):
	'''
	GET /api/v3/dhcp/dynamic_lease/
	'''
	dynamic_lease=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}dhcp/dynamic_lease/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			dynamic_lease=response['result']
		except KeyError:
			static_lease=None
	else:
		app.err_log.append((response['error_code'], response['msg']))
			
	return dynamic_lease
