#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/wifi/
'''
import requests
import json


def get_config(app):
	'''
	GET /api/v2/wifi/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/config/'.format(
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
	PUT /api/v2/wifi/config/
	
	dict() config (example):
	{
	   "enabled": false
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}wifi/config/'.format(
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


def reset_config(app):
	'''
	POST /api/v2/wifi/config/reset/
	'''
	reset=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}wifi/config/reset/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		reset=True
	
	return reset


def get_ap_config(app, _id=''):
	'''
	GET /api/v2/wifi/ap/{id}
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/ap/{}'.format(
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
	
	return config


def update_ap_config(app, config, _id):
	'''
	PUT /api/v2/wifi/ap/{id}
	
	dict() config (example):
	{
		"config": {
			"channel_width": "20",
			"ht": {
				"ht_enabled": false
			},
			"primary_channel": 0,
			"secondary_channel": 0
		}
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}wifi/ap/{}'.format(
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
	
	return update


def get_ap_bss(app, _id=''):
	'''
	GET /api/v2/wifi/bss/
	'''
	bss=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/bss/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			bss=response['result']
		except KeyError:
			bss=None
	
	return station


def update_ap_bss(app, config, _id):
	'''
	PUT /api/v2/wifi/bss/{id}
	
	dict() config (example):
	{
		"config": {
			"key": "c'était trop facile"
		}
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}wifi/bss/{}'.format(
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
	
	return update
	

def get_station_connected(app, _id):
	'''
	GET /api/v2/wifi/ap/{id}/stations/
	
	_id: id of AP.
	'''
	station=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/ap/{}/stations/'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			station=response['result']
		except KeyError:
			station=None
	
	return station


def get_ap_neighbors(app, _id):
	'''
	GET /api/v2/wifi/ap/{id}/neighbors/
	'''
	neighbors=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/ap/{}/neighbors/'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			neighbors=response['result']
		except KeyError:
			neighbors=None
	
	return neighbors


def get_config_macfilter(app, _id=''):
	'''
	GET /api/v2/wifi/mac_filter/{id}
	'''
	mac_filter=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}wifi/mac_filter/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			mac_filter=response['result']
		except KeyError:
			mac_filter=None
	
	return mac_filter


def update_macfilter(app, config, _id):
	'''
	PUT /api/v2/wifi/mac_filter/{filter_id}
	
	dict() config (example):
	{
	   "comment": "filtre de test",
	   "type": "blacklist"
	}
	'''
	update=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}wifi/mac_filter/{}'.format(
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
	
	return update
	

def create_macfilter(app, config):
	'''
	POST /api/v2/wifi/mac_filter/
	
	dict() config (example):
	{
	   "comment": "filtre de test",
	   "type": "blacklist",
	   "mac": "00:07:CB:CB:07:00"
	}
	'''
	create=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}wifi/mac_filter/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			create=response['result']
		except KeyError:
			create=None
	
	return create
	

def delete_macfilter(app, _id):
	'''
	DELETE /api/v2/wifi/mac_filter/{id}
	'''
	delete=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}wifi/mac_filter/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		delete=True
	
	return delete
	
