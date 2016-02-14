#!/usr/bin/env python

import requests
import json
import hmac

from fbxtools.Application import Application


def init_app(app_details='app_details.json', app_token='app_token.json'):
	init=False
	
	#Get version and base url of API.
	result=get_api_config()
	api_version=float(result['api_version'])
	api_base_url=result['api_base_url']+str(int(float(result['api_version'])))+'/'
	
	#get app configuration.
	with open(app_details, 'r') as f:    
		app=json.load(f)
		
		r=requests.post(
			'http://mafreebox.freebox.fr{}login/authorize/'.format(
				api_base_url
			), 
			headers = {'content-type': 'application/json'},
			data=json.dumps(app)
		)
		
		response=r.json()

		if response['success']:
			init=True
			
			#Copy token and track_id.
			with open(app_token, 'w') as f:
				json.dump(response['result'], f)
				
				print('[fxb-tools] > Appuyez sur la touche ">" de votre freebox pour autoriser <%s>'%app['app_name'])
				
	return init


def connect_app(app_details='app_details.json', app_token='app_token.json'):
	connect=False
	
	app=Application()
	
	#Get version and base url of API.
	result=get_api_config()
	app.api_version=float(result['api_version'])
	app.api_base_url=result['api_base_url']+'v'+str(int(app.api_version))+'/'
	
	#get app configuration.
	with open(app_details, 'r') as f:    
		config=json.load(f)
		
		app.name=config['app_name']
		app.id=config['app_id']
		app.version=config['app_version']
		
		with open(app_token, 'r') as f:    
			app_infos=json.load(f)
				
			r=requests.get(
				'http://mafreebox.freebox.fr{}login/authorize/{}'.format(
					app.api_base_url, 
					app_infos['track_id']
				),
				headers={ 'X-Fbx-App-Auth': app_infos['app_token']}
			)
			
			response=r.json()
			challenge=response['result']['challenge']
			
			#Create password and login dict.
			h=hmac.new(app_infos['app_token'].encode(), challenge.encode(), 'sha1')
			password=h.hexdigest()
			auth_details={'app_id':config['app_id'], 'password':password}
			
			#Login.
			r=requests.post(
				'http://mafreebox.freebox.fr{}login/session/'.format(
					app.api_base_url
				), 
				headers={'content-type': 'application/json', 'X-Fbx-App-Auth': app_infos['app_token']},
				data=json.dumps(auth_details),
			)

			response=r.json()
			
			if response['success']:
				app.set_permission(response['result']['permissions']) #Define permissions.
				app.session_token=response['result']['session_token']
				
				connect=app
			else:
				print('[{}] {}'.format(response['error_code'], response['msg']))
		
	return connect


def deconnect_app(app):
	deconnect=False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}login/logout/'.format(
			app.api_base_url
		),
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	response=r.json()
	
	if response['success']:
		deconnect=True
	
	return deconnect

	
def get_api_config():
	'''
	GET /api_version
	'''
	
	r=requests.get('http://mafreebox.freebox.fr/api_version')
	response=r.json()
	
	return response
	
