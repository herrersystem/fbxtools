#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import hmac, hashlib
from apize.apize import Apize
from fbxtools.exceptions import *
from fbxtools.utils import *


class Fbx():
	def __init__(self, url, app_infos='app_infos.json', 
		app_auth='app_auth.json', verify_cert=False):
			self.url = url
			self.api = Apize(self.url)
			self.api.verify_cert = verify_cert
			self.app_auth = app_auth
			self.app_infos = app_infos


	def init_app(self, infos):
		@self.api.call('/login/authorize/', method='POST')
		def wrapper(infos):
			return {'data': infos, 'is_json': True}
		return wrapper(infos)


	def connect_app(self, app_token, app_id, challenge):
		@self.api.call('/login/session/', method='POST')
		def wrapper(app_token, app_id, challenge):
			h = hmac.new(app_token.encode(), challenge, hashlib.sha1)
			password = h.hexdigest()
			data = {'app_id': app_id, 'password': password}
			headers = {'X-Fbx-App-Auth': app_token}
			return {'data': data, 'headers': headers, 'is_json': True}
		return wrapper(app_token, app_id, challenge)


	def disconnect_app(self):
		@self.api.call('/logout/')
		def wrapper():
			return {}
		return wrapper()


	def get_challenge(self):
		@self.api.call('/login/')
		def wrapper():
			return {}
		return wrapper()


	def get_session_token(self):
		"""Authenticate your app to allow use API."""
		response = self.get_challenge()
		if not response['data']['success']:
			raise FbxSessionToken(
				response['data']['error_code'],
				response['data']['error_code']
			)
		challenge = response['data']['result']['challenge'].encode()
		auth = parse_auth_file(self.app_auth)
		infos = parse_auth_file(self.app_infos)
		conn = self.connect_app(auth['app_token'], infos['app_id'], 
			challenge)
		if not conn['data']['success']:
			raise FbxSessionToken(
				response['data']['error_code'],
				response['data']['error_code']
			)
		session_token = conn['data']['result']['session_token']
		self.api.headers['X-Fbx-App-Auth'] = session_token 
		return session_token


	def get_app_token(self):
		"""Allow and register your app to the Freebox Server."""
		infos = parse_infos_file(self.app_infos)
		response = self.init_app(infos)['data']
		if response['success']:
			with open(self.app_auth, 'w') as f:
				content = json.dumps(response['result'])
				f.write(content)
		else:
			raise FbxAppToken(
				response['data']['error_code'],
				response['data']['error_code']
			)
		return (response['result']['app_token'], 
			response['result']['track_id'])


	def track_auth_progress(self, track_id):
		@self.api.call('/login/authorize/:id')
		def wrapper(track_id):
			args = {'id': track_id}
			return {'args': args}
		return wrapper(track_id)
