#!/usr/bin/env python
'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/system/
'''
import requests
import json


def get_system_info(app):
	'''
	GET /api/v3/system/
	'''
	infos=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}system/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			infos=response['result']
		except KeyError:
			infos=None
	
	return infos


def reboot_system(app):
	'''
	POST /api/v3/system/reboot/
	'''
	reboot=False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}system/reboot/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		reboot=True
	
	return reboot
	
