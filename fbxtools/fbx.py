#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import print_function

import hmac
from hashlib import sha1
from apize.apize import Apize
from fbxtools.exceptions import *
from fbxtools.utils import *
from fbxtools.fbxo import *

import time
from datetime import timedelta, datetime

class Fbx():

	def __init__(self, url, app_infos='app_infos.json', 
		app_auth='app_auth.json', verify_cert=False, mute=False):
		
		self.url = url
		self.api = Apize(self.url)
		self.api.verify_cert = verify_cert
		self.app_auth = app_auth
		self.app_infos = app_infos
		self.mute = mute

		self._permissions = Permissions()
		for field_name in ["pvr","explorer","calls","contacts","tv","parental","settings","downloader"]:
			setattr(self._permissions,field_name,False)
		
		self._boxinfos = Boxinfos()
		self._boxinfos.boxinfos_loaded = False
		self._calls	= {}
		self._contacts = {}
		self._groups = {}

		self._boxinfos_loaded = False

	def init_app(self, infos):
		@self.api.call('/login/authorize/', method='POST')
		def wrapper(infos):
			return {'data': infos, 'is_json': True}

		return wrapper(infos)


	def connect_app(self, app_token, app_id, challenge):
		@self.api.call('/login/session/', method='POST')
		def wrapper(app_token, app_id, challenge):
			h = hmac.new(app_token.encode(), challenge, sha1)
			password = h.hexdigest()

			data = {'app_id': app_id, 'password': password}
			headers = {'X-Fbx-App-Auth': app_token}

			return {
				'data': data,
				'headers': headers,
				'is_json': True
			}

		return wrapper(app_token, app_id, challenge)


	def get_challenge(self, track_id):
		@self.api.call('/login/authorize/:id')
		def wrapper(track_id):
			args = {'id': track_id}

			return {'args': args}

		return wrapper(track_id)


	def get_session_token(self):
		"""
		Authenticate your app to allow use API.
		"""
		auth = parse_auth_file(self.app_auth)
		response = self.get_challenge(auth['track_id'])

		if not response['data']['success']:
			raise FbxSessionToken(
				response['data']['error_code'],
				response['data']['error_code']
			)

		challenge = response['data']['result']['challenge'].encode()
		infos = parse_auth_file(self.app_infos)
		conn = self.connect_app(
			auth['app_token'], 
			infos['app_id'], 
			challenge
		)

		if not conn['data']['success']:
			raise FbxSessionToken(
				response['data']['error_code'],
				response['data']['error_code']
			)

		session_token = conn['data']['result']['session_token']
		permissions = conn['data']['result']['permissions']
		for permission in permissions:
			if permission == 'pvr':
				self._permissions.pvr = permissions[permission]
			elif permission == 'explorer':
				self._permissions.explorer = permissions[permission]
			elif permission == 'calls':
				self._permissions.calls = permissions[permission]
			elif permission == 'contacts':
				self._permissions.contacts = permissions[permission]
			elif permission == 'tv':
				self._permissions.tv = permissions[permission]
			elif permission == 'parental':
				self._permissions.parental = permissions[permission]
			elif permission == 'settings':
				self._permissions.settings = permissions[permission]
			elif permission == 'downloader':
				self._permissions.downloader = permissions[permission]
		self.api.headers['X-Fbx-App-Auth'] = session_token 

		return session_token

	def get_status(self, track_id):
		@self.api.call('/login/authorize/:id')
		def wrapper(track_id):
			args = {'id': track_id}
			return {'args': args}
		return wrapper(track_id)		
	
	def get_app_token(self):
		"""
		Allow and register your app to the Freebox Server.
		"""
		infos = parse_infos_file(self.app_infos)
		response = self.init_app(infos)['data']
		
		if not self.mute:
			print (response)

		if response['success']:
			with open(self.app_auth, 'w') as f:
				content = json.dumps(response['result'])
				track_id = response['result']['track_id']
				f.write(content)
				
				if not self.mute:
					print('%s file was generated.' % self.app_auth)
					print('Press ">" button on the dial of the Freebox')
					
				# Track authorization progress
				status = "pending"
				count = 0
				while (status!="granted") and (count<20):
					count += 1
					response1 = self.get_status(track_id)['data']
					if not self.mute:
						print (response1)
					if response['success']:
						status = response1['result']['status']
					time.sleep(2)
					
		else:
			raise FbxAppToken(
				response['data']['error_code'],
				response['data']['error_code']
			)

		return (
			response['result']['app_token'],
			response['result']['track_id']
		)
	
	def get_system(self):
		@self.api.call('/system/')
		def wrapper():
			return {}

		return wrapper()
	
	def _system_reboot(self):
		@self.api.call('/system/reboot/',method='POST')
		def wrapper():
			return {}

		return wrapper()
	
	def system_reboot(self,reboot=False):
		if reboot:
			data = self._system_reboot()
			try:
				return data['success']
			except:
				return False
		else:
			return False
	
	def _build_boxinfos(self,data):
		boxinfos = Boxinfos()
		for index in data:
			if index == "uptime_val":
				setattr(boxinfos,index,timedelta(seconds=data[index]))
			else:
				setattr(boxinfos,index,data[index])
		setattr(boxinfos,"boxinfos_loaded",True)
		return boxinfos
	
	
	def get_boxinfos(self):
		data = self.get_system()['data']
		if data['success']:
			boxinfos = self._build_boxinfos(data['result'])
		return boxinfos
				
	def get_permissions(self):
		return self._permissions
	
	def _build_callinfos(self,call):
		call_type = getattr(call,'type')
		if call_type == 'missed':
			setattr(call,'missed',True)
			setattr(call,'accepted',False)
			setattr(call,'outgoing',False)
		elif call_type == 'accepted':
			setattr(call,'missed',False)
			setattr(call,'accepted',True)
			setattr(call,'outgoing',False)
		elif call_type == 'outgoing':
			setattr(call,'missed',False)
			setattr(call,'accepted',False)
			setattr(call,'outgoing',True)

		return call
	

	def get_permissions(self):
		return self._permissions
		
	#
	# get fbx list object
	#	

	def get_contacts_all(self):
		return self.get_contacts()
	
	def get_contacts(self,start=0,limit=-1,page=1,group_id=None):
		if not self.permissions.contacts :
			self._contacts = []
			return self._contacts
		contacts = Contacts(fbx=self)
		params = {'start':start,'limit':limit,'page':page,'group_id':group_id}
		self._contacts = contacts.get_by_id(params=params)
		return self._contacts.contacts

	def get_groups(self):
		if not self.permissions.contacts :
			self._groups = []
			return self._groups.groups
		groups = Groups(fbx=self)
		self._groups = groups.get_by_id()
		return self._groups.groups

	def get_calls(self):
		if not self.permissions.contacts :
			self._calls = []
			return self._calls.calls
		calls = Calls(fbx=self)
		self._calls = calls.get_by_id()
		for call in self._calls.calls:
			self._build_callinfos(call)
		return self._calls.calls

	def get_interfaces(self):
		if not self.permissions.explorer :
			self._interfaces = []
			return self._interfaces.interfaces
		interfaces = Interfaces(fbx=self)
		self._interfaces = interfaces.get_by_id()
		return self._interfaces.interfaces	

	def get_lanhosts(self,args=None):
		if not self.permissions.explorer :
			self._lanhosts = []
			return self._lanhosts.lanhosts
		lanhosts = LanHosts(fbx=self)
		self._lanhosts = lanhosts.get_by_id(args=args)
		return self._lanhosts.lanhosts	


	#
	# get fbx object
	#
			
	def _get_fbobj(self,Fbobjclass,id=None,permission=True):
		if not permission : return Fbobjclass()
		fbxobj = Fbobjclass(fbx=self)
		fbxobj = fbxobj.get_by_id(id=id)
		return fbxobj
	
	def get_contact(self,contact_id):
		return self._get_fbobj(Contact,id=contact_id,\
								permission=self.permissions.contacts)
		
	def get_address(self,address_id):
		return self._get_fbobj(Address,address_id,\
								permission=self.permissions.contacts)
		
	def get_number(self,number_id):
		return self._get_fbobj(Number,id=number_id,\
								permission=self.permissions.contacts)
		
	def get_email(self,email_id):
		return self._get_fbobj(Email,id=email_id,\
								permission=self.permissions.contacts)
		
	def get_url(self,url_id):
		return self._get_fbobj(Url,id=url_id,\
								permission=self.permissions.contacts)
		
	def get_group(self,group_id):
		return self._get_fbobj(Group,id=group_id,\
								permission=self.permissions.contacts)
		
	def get_call(self,call_id):
		return self._get_fbobj(Call,id=call_id,\
								permission=self.permissions.calls)
	#
	# set fbx object
	#		

	def _set_fbobj(self,Fbobjclass,id,data,permission=True):
		if not permission : return Fbobjclass()
		fbxobj = Fbobjclass(fbx=self)
		fbxobj = fbxobj.set_by_id(id,data)
		return fbxobj
	
	def set_contact(self,contact_id,contactinfos):
		return self._set_fbobj(Contact,contact_id,contactinfos,\
								self.permissions.contacts)
	
	def set_address(self,address_id,addressinfos):
		return self._set_fbobj(Address,address_id,addressinfos,\
								self.permissions.contacts)
	
	def set_number(self,number_id,numberinfos):
		return self._set_fbobj(Number,number_id,numberinfos,\
								self.permissions.contacts)
	
	def set_email(self,email_id,emailinfos):
		return self._set_fbobj(Email,email_id,emailinfos,\
								self.permissions.contacts)
	
	def set_url(self,url_id,urlinfos):
		return self._set_fbobj(Url,url_id,urlinfos,\
								self.permissions.contacts)
	
	def set_group(self,group_id,groupinfos):
		return self._set_fbobj(Group,group_id,groupinfos,\
								self.permissions.contacts)
	
	def set_call(self,call_id,callinfos):
		return self._set_fbobj(Call,call_id,callinfos,\
								self.permissions.calls)

	#
	# new fbx object
	#
	
	def _new_fbobj(self,Fbobjclass,data,permission=True):
		if not permission : return Fbobjclass()
		fbxobj = Fbobjclass(fbx=self)
		fbxobj = fbxobj.new_fbxobj(data)
		return fbxobj
	
	def new_contact(self,contactinfos):
		return self._new_fbobj(Contact,contactinfos,self.permissions.contacts)
	
	def new_number(self,numberinfos):
		return self._new_fbobj(Number,numberinfos,self.permissions.contacts)
	
	def new_address(self,addressinfos):
		return self._new_fbobj(Address,addressinfos,self.permissions.contacts)
	
	def new_email(self,emailinfos):
		return self._new_fbobj(Email,emailinfos,self.permissions.contacts)
	
	def new_url(self,urlinfos):
		return self._new_fbobj(Url,urlinfos,self.permissions.contacts)
	
	def new_group(self,groupinfos):
		return self._new_fbobj(Group,groupinfos,self.permissions.contacts)
	
	#
	# delete fbx object
	#								
	
	def _delete_fbobj(self,Fbobjclass,id,permission=True):
		if not permission : return Fbobjclass()
		fbxobj = Fbobjclass(fbx=self)
		return fbxobj.delete_by_id(id=id)	
	
	def delete_contact(self,contact_id):
		return self._delete_fbobj(Contact,contact_id,\
								self.permissions.contacts)	
	
	def delete_number(self,number_id):
		return self._delete_fbobj(Number,number_id,\
								self.permissions.contacts)
	
	def delete_address(self,address_id):
		return self._delete_fbobj(Address,address_id,\
								self.permissions.contacts)
	
	def delete_email(self,email_id):
		return self._delete_fbobj(Email,email_id,\
								self.permissions.contacts)	
	
	def delete_url(self,url_id):
		return self._delete_fbobj(Url,url_id,\
								self.permissions.contacts)
	
	def delete_group(self,group_id):
		return self._delete_fbobj(Group,group_id,\
								self.permissions.contacts)
	
	def delete_call(self,call_id):
		return self._delete_fbobj(Call,call_id,\
								self.permissions.calls)						
								

	permissions = property(get_permissions, None, None, "freebox app permissions Permissions")
	calls	    = property(get_calls, None, None, "freebox calls list")
	contacts    = property(get_contacts_all, None, None, "freebox contacts list")
	groups	    = property(get_groups, None, None, "freebox groups list")
	boxinfos	= property(get_boxinfos, None, None, "freebox infos Boxinfos")
	interfaces  = property(get_interfaces, None, None, "freebox interfaces list")
	
	def __str__(self):
		fbstr = u"uptime: %s, disk_status: %s\r\nfirmware_version: %s, box_authenticated: %s\r\n"\
		% (self.boxinfos.uptime,self.boxinfos.disk_status,self.boxinfos.firmware_version,self.boxinfos.box_authenticated)
		fbstr += u"fan_rpm: %s RPM, temp_cpub: %s °C, temp_cpum: %s °C, temp_sw: %s °C\r\n"\
		% (self.boxinfos.fan_rpm,self.boxinfos.temp_cpub,self.boxinfos.temp_cpum,self.boxinfos.temp_sw)
		fbstr += u"board_name: %s, mac: %s, serial: %s"\
		% (self.boxinfos.board_name,self.boxinfos.mac,self.boxinfos.serial)
		return fbstr			
