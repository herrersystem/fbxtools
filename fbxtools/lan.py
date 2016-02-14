#!/usr/bin/env python

'''
Freebox API
for more infos : http://dev.freebox.fr/sdk/os/lan/
'''
import requests
import json


def get_config(app):
	'''
	GET /api/v3/lan/config/
	'''
	config=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}lan/config/'.format(
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
	

def get_interfaces(app):
	'''
	GET /api/v3/lan/browser/interfaces/
	'''
	interfaces=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}lan/browser/interfaces/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			interfaces=response['result']
		except KeyError:
			interfaces=None
	
	return interfaces


def get_hosts(app, interface, _id=''):
	'''
	GET /api/v3/lan/browser/{interface}/
	
	str() interface (example): pub
	'''
	hosts=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}lan/browser/{}/{}'.format(
			app.api_base_url, 
			interface,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			hosts=response['result']
		except KeyError:
			hosts=None
	
	return hosts


def update_host(app, interface, config, _id):
	'''
	PUT /api/v3/lan/browser/{interface}/{hostid}/
	
	dict() config (example):
	
	{
	   "id":"ether-00:24:d4:7e:00:4c",
	   "primary_name":"Freebox Tv"
	}
	'''
	change=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}lan/browser/{}/{}'.format(
			app.api_base_url, 
			interface, 
			_id
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			change=response['result']
		except KeyError:
			change=None
	
	return response
