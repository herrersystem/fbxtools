#!/usr/bin/env python

'''
Freebox OS API
for more infos : http://dev.freebox.fr/sdk/os/contacts/
'''
import requests
import time
import json


def get_contacts(app, _id=''):
	'''
	GET /api/v3/contact/{id}
	'''
	contacts=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.get(
		'http://mafreebox.freebox.fr{}contact/'.format(
			app.api_base_url,
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contacts=response['result']
		except KeyError:
			contacts=None
	
	return contacts


def update_contact(app, infos, _id):
	'''
	PUT /api/v3/contact/{id}
	
	dict() infos (examples):
	
	{"company": "Standard Oil"}
	
	or
	
	{
		"display_name": "evil",
		"last_name": "Rockfeller",
		"company": "Standard Oil"
	}
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}contact/{}'.format(
			app.api_base_url,
			_id
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact


def create_contact(app, infos):
	'''
	POST /api/v3/contact/
	
	dict() infos (examples):
	
	{
		"display_name": "Sandy Kilo",
		"first_name": "Sandy",
		"last_name":"Kilo"
	}
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}contact/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact


def delete_contact(app, _id):
	'''
	DELETE /api/v3/contact/{id}
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}contact/{}'.format(
			app.api_base_url, 
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		contact=True
			
	return contact


def create_number(app, infos):
	'''
	POST /api/v3/number/
	
	dict() infos (examples):
	
	{
	   "contact_id": 1,
	   "number": "0144456789",
	   "type": "fixed"
	}	
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}number/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact


def create_email(app, infos):
	'''
	POST /api/v3/email/
	
	dict() infos (examples):
	
	{
		"contact_id": 1,
		"email": "test@test.fr",
		"type": "home"
	}
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}email/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact


def create_address(app, infos):
	'''
	POST /api/v3/address/
	
	dict() infos (examples):
	
	{
		"contact_id": 1,
		"country": "France",
		"city": "Paris",
		"zipcode": "75008",
		"street": "8 rue du pont",
		"street2": "",
		"number": "11",
		"type": "home",
	}
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.post(
		'http://mafreebox.freebox.fr{}address/'.format(
			app.api_base_url
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact


def update_information(app, _type, _id):
	'''
	PUT /api/v3/[number,address,url,email]/{id}
	
	str() _type: number or email or address
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.put(
		'http://mafreebox.freebox.fr{}{}/{}'.format(
			app.api_base_url,
			_type,
			_id
		), 
		headers={'content-type': 'application/json','X-Fbx-App-Auth': app.session_token},
		data=json.dumps(infos)
	)
	
	response=r.json()
	
	if response['success']:
		try:
			contact=response['result']
		except KeyError:
			contact=None
			
	return contact	


def delete_information(app, _type, _id):
	'''
	DELETE /api/v3/[number,address,email]/{id}
	
	str() _type: number or email or address
	'''
	contact=False
	
	if not app.AUTH_CONTACTS:
		app.err_log.append(('err_auth', 'not allowed : AUTH [CONTACTS]')
		return False
	
	r=requests.delete(
		'http://mafreebox.freebox.fr{}{}/{}'.format(
			app.api_base_url, 
			_type, 
			_id
		), 
		headers={'X-Fbx-App-Auth': app.session_token}
	)
	
	response=r.json()
	
	if response['success']:
		contact=True
	
	return contact

