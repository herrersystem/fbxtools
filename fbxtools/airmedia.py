#!/usr/bin/env python

'''
Freebox API
for more infos : http://dev.freebox.fr/sdk/os/airmedia/
'''
import requests
import json


def get_config(app):
	'''
	GET /api/v3/airmedia/receivers/
	
	Get the list of AirMediaReceiver connected to the Freebox Server.
	'''
	receivers=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}airmedia/receivers/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token},
	)
	
	response=r.json()
	if response['success']:
		try:
			receivers=response['result']
		except KeyError:
			receivers=None
	
	return receivers
	

def get_current_config(app):
	'''
	GET /api/v3/airmedia/config/
	'''
	receiver=False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}airmedia/config/'.format(
			app.api_base_url
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	if response['success']:
		try:
			receiver=response['result']
		except KeyError:
			receiver=None
	
	return receiver


def update_current_config(app, config):
	'''
	PUT /api/v3/airmedia/
	'''
	receiver=False
	
	if not app.AUTH_SETTINGS:
		print('[fbx-tools] > Not Allowed [SETTINGS]')
		return -1
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}airmedia/config/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(config)
	)
	
	response=r.json()
	if response['success']:
		try:
			receiver=response['result']
		except KeyError:
			receiver=None
	
	return receiver
	

def play_media(app, media, receiver='Freebox Server'):
	'''
	POST /api/v3/airmedia/receivers/Freebox%20Player/
	
	dict() media (example):
	{
	   "action": "start",
	   "media_type": "video",
	   "media": "http://anon.nasa-global.edgesuite.net/HD_downloads/GRAIL_launch_480.mov"
	}
	'''	
	play=False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}airmedia/receivers/{}/'.format(
			app.api_base_url,
			receiver
		), 
		headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app.session_token},
		data=json.dumps(media)
	)
	
	response=r.json()
	if response['success']:
		play=True
		
	return play
