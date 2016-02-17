#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/connection/
'''
import requests
import json


def get_status(app):
	'''
	GET /api/v3/connection/
	'''
	status=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			status=response['result']
		except KeyError:
			status=None
	
	return status


def get_config(app):
	'''
	GET /api/v3/connection/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/config/'.format(
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
	PUT /api/v3/connection/config/
	
	dict() config (example):
	{
		"ping": true,
		"wol": false
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}connection/config/'.format(
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


def get_ipv6_config(app):
	'''
	GET /api/v3/connection/ipv6/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/ipv6/config/'.format(
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


def update_ipv6_config(app, config):
	'''
	PUT /api/v3/connection/ipv6/config/
	
	dict() config (example):
	{
	   "delegations": [
			{
				"prefix": "2a01:e30:d252:a2a2::/64",
				"next_hop": "fe80::be30:5bff:feb5:fcc7"
			}
	   ]
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}connection/ipv6/config/'.format(
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


def get_ddns_status(app, provider):
	'''
	GET /api/v3/connection/ddns/{provider}/status/
	
	str() provider: ovh, dyndns, noip.
	'''
	status=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/ddns/{}/status/'.format(
			app.api_base_url,
			provider
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			status=response['result']
		except KeyError:
			status=None
	
	return status


def get_ddns_config(app, provider):
	'''
	GET /api/v3/connection/ddns/{provider}/
	
	str() provider: ovh, dyndns, noip.
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/ddns/{}/'.format(
			app.api_base_url,
			provider
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


def update_ddns_config(app, config, provider):
	'''
	PUT /api/v3/connection/ddns/{provider}/
	
	dict() config (example):
	{
		"enabled": false,
		"user": "test",
		"password": "ssss",
		"hostname": "ttt"
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
		
	r=requests.put(
		'http://mafreebox.freebox.fr{}connection/ddns/{}/'.format(
			app.api_base_url,
			provider
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


def get_xdsl_config(app):
	'''
	GET /api/v3/connection/xdsl/ [UNSTABLE]
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/xdsl/{}/'.format(
			app.api_base_url,
			provider
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
	

def get_ftth_status(app):
	'''
	GET /api/v3/connection/ftth/ [UNSTABLE]
	'''
	status=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}connection/ftth/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			status=response['result']
		except KeyError:
			status=None
	
	return status	
