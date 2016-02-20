#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/call/
'''
import requests
import time


def get_dmz_config(app):
	'''
	GET /api/v3/fw/dmz/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}fw/dmz/'.format(
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


def update_dmz_config(app, config):
	'''
	PUT /api/v3/fw/dmz/
	
	dict() config (example):
	{
	   "enabled": true,
	   "ip": "192.168.1.42"
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}fw/dmz/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app.session_token},
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


def get_portfw_config(app, _id=''):
	'''
	GET /api/v3/fw/redir/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}fw/redir/{}'.format(
			app.api_base_url,
			_id
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


def update_dmz_config(app, config, _id):
	'''
	PUT /api/v3/fw/redir/{redir_id}
	
	dict() config (example):
	{
	  "enabled": false
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}fw/redir/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app.session_token},
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


def add_portfw(app, config):
	'''
	POST /api/v3/fw/redir/
	
	dict() config (example):
	{
		"enabled": true,
		"comment": "test",
		"lan_port": 4242,
		"wan_port_end": 4242,
		"wan_port_start": 4242,
		"lan_ip": "192.168.1.42",
		"ip_proto": "tcp",
		"src_ip": "0.0.0.0"
	}
	'''
	portfw=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}fw/redir/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			portfw=response['result']
		except KeyError:
			portfw=None
	else:
		app.err_log.append((response['error_code'], response['msg']))
		
	return portfw


def delete_portfw(app, _id):
	'''
	DELETE /api/v3/fw/redir/{redir_id}
	'''
	delete=False
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}fw/redir/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			delete=response['result']
		except KeyError:
			delete=None
	else:
		app.err_log.append((response['error_code'], response['msg']))
		
	return delete


def get_inport_config(app, _id=''):
	'''
	GET /api/v3/fw/incoming/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}fw/incoming/{}'.format(
			app.api_base_url,
			_id
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


def update_inport_config(app, config, _id):
	'''
	PUT /api/v3/fw/incoming/{port_id}
	
	dict() config (example):
	{
	  "in_port": 3615
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [SETTINGS]'))
		return False
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}fw/incoming/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app.session_token},
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
