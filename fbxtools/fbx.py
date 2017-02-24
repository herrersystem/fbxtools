#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import print_function

import hmac
from hashlib import sha1
from apize.apize import Apize
from fbxtools.exceptions import *
from fbxtools.utils import *

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
		self._calls    = {}
		self._contacts = {}
		self._groups = {}

		self._boxinfos_loaded = False
		self._uptime = timedelta(days=0) 
		self._disk_status = "" 
		self._fan_rpm = 0
		self._temp_cpub = 0
		self._uptime_val = 0 
		self._board_name = "" 
		self._mac = "" 
		self._temp_cpum = 0
		self._temp_sw = 0
		self._box_authenticated = False
		self._serial = ""
		self._firmware_version = ""

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
		@self.api.call('/system/reboot/')
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
		return boxinfos
	
	
	def get_system_infos(self):
		data = self.get_system()['data']
		if data['success']:
			boxinfos = self._build_boxinfos(data['result'])
			print("BoxInfos:%s" % boxinfos)
			self._uptime      = data['result']['uptime']
			self._disk_status = data['result']['disk_status'] 
			self._fan_rpm	  = data['result']['fan_rpm']
			self._temp_cpub   = data['result']['temp_cpub']
			self._uptime_val  = timedelta(seconds=data['result']['uptime_val'])
			self._board_name  = data['result']['board_name']
			self._mac	  = data['result']['mac'] 
			self._temp_cpum   = data['result']['temp_cpum']
			self._temp_sw	  = data['result']['temp_sw']
			self._box_authenticated = data['result']['box_authenticated']
			self._serial      = data['result']['serial']
			self._firmware_version  = data['result']['firmware_version']
			self._boxinfos_loaded = True
		return data
	
	def _get_system_info(self):
		if self._boxinfos_loaded:
			return True
		data = self.get_system_infos()
		if data['success']:
			return self._boxinfos_loaded
		return False
			
		
	
	def get_uptime(self):
		if self._get_system_info():
			return self._uptime
		else:
			return ""
		
	def get_fan_rpm(self):
		if self._boxinfos_loaded:
			return self._fan_rpm
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._fan_rpm
			else:
				return 0
		
	def get_disk_status(self):
		if self._boxinfos_loaded:
			return self._disk_status
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._disk_status
			else:
				return 0
		
	def get_temp_cpub(self):
		if self._boxinfos_loaded:
			return self._temp_cpub
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._temp_cpub
			else:
				return 0
		
	def get_uptime_val(self):
		if self._boxinfos_loaded:
			return self._uptime_val
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._uptime_val
			else:
				return 0
		
	def get_board_name(self):
		if self._boxinfos_loaded:
			return self._board_name
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._board_name
			else:
				return ""
		
	def get_mac(self):
		if self._boxinfos_loaded:
			return self._mac
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._mac
			else:
				return ""
		
	def get_temp_cpum(self):
		if self._boxinfos_loaded:
			return self._temp_cpum
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._temp_cpum
			else:
				return 0
		
	def get_temp_sw(self):
		if self._boxinfos_loaded:
			return self._temp_sw
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._temp_sw
			else:
				return 0
		
	def get_box_authenticated(self):
		if self._boxinfos_loaded:
			return self._box_authenticated
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._box_authenticated
			else:
				return False
		
	def get_serial(self):
		if self._boxinfos_loaded:
			return self._serial
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._serial
			else:
				return ""
		
	def get_firmware_version(self):
		if self._boxinfos_loaded:
			return self._firmware_version
		else:
			uptime = self.uptime
			if self._uptime != timedelta(days=0):
				return self._firmware_version
			else:
				return ""
			
	def get_permissions(self):
		return self._permissions
	
	def _get_calls(self):
		@self.api.call('/call/log/')
		def wrapper():
			return {}

		return wrapper()

	def _get_call(self,call_id):
		@self.api.call('/call/log/:id')
		def wrapper():
			args = {'id': call_id}
			return {'args': args}

		return wrapper()
	
	def _build_callinfos(self,call):
		callinfos = Call()
		for index in call:
			if index == "datetime":
				setattr(callinfos,index,datetime.fromtimestamp(call[index]))
			elif index == "duration":
				setattr(callinfos,index,timedelta(seconds=call[index]))
			elif index == "type":
				setattr(callinfos,index,call[index])
				if call[index] == 'missed':
					setattr(callinfos,'missed',True)
				else:
					setattr(callinfos,'missed',False)
				if call[index] == 'accepted':
					setattr(callinfos,'accepted',True)
				else:
					setattr(callinfos,'accepted',False)
				if call[index] == 'outgoing':
					setattr(callinfos,'outgoing',True)
				else:
					setattr(callinfos,'outgoing',False)
			else:
				setattr(callinfos,index,call[index])
		return callinfos
	
	
	def get_calls(self,call_id=None):
		result = {}
		if not self.permissions.calls :
			return result
		if call_id==None:
			data = self._get_calls()['data']
			if not data['success']:
				return result
			self._calls = {}
			calls = data['result']
			for call in calls:
				callinfos = self._build_callinfos(call)
				self._calls[call['id']] = callinfos
			return self._calls
		else:
			data = self._get_call(call_id)['data']
			#print(data)
			if not data['success']:
				return result
			call = data['result']
			callinfos = self._build_callinfos(call)
			return callinfos

	def _get_contacts(self,start=0,limit=-1,group_id=None):
		@self.api.call('/contact/')
		def wrapper():
			data = {'start': start, 'limit': limit, 'group_id': group_id}
			print(data)
			return {'data': data}

		return wrapper()

	def _get_contact(self,contact_id):
		@self.api.call('/contact/:id')
		def wrapper():
			args = {'args': contact_id}
			return {'args': data}

		return wrapper()
	
	
	def _build_contactinfos(self,contact):
		contactinfos = Contact()
		for index in contact:
			if index == "last_update":
				setattr(contactinfos,index,datetime.fromtimestamp(contact[index]))
			elif index == "duration":
				setattr(contactinfos,index,timedelta(seconds=contact[index]))
			else:
				setattr(contactinfos,index,contact[index])
		return contactinfos
	
	def get_contact(self,contact_id):
		data = self._get_contact(contact_id)['data']
		#print(data)
		if not data['success']:
			return result
		contact = data['result']
		contactinfos = self._build_contactinfos(contact)
		return contactinfos
	
	def get_contacts(self,start=0,limit=-1,group_id=None):
		result = {}
		if not self.permissions.contacts :
			return result
		data = self._get_contacts(start,limit,group_id)['data']
		#print(data)
		try:
			if not data['success']:
				return result
		except KeyError:
			return result
		contacts = data['result']
		self._contacts = {}
		#☺print(contacts)
		for contact in contacts:
			contactinfos = self._build_contactinfos(contact)
			if group_id!=None:
				self._contacts[contact['id']] = contactinfos
			else:
				self._contacts[contact['id']] = contactinfos
		return self._contacts

	def _get_groups(self):
		@self.api.call('/group/')
		def wrapper():
			return {}

		return wrapper()
	
	def _build_groupinfos(self,group):
		groupinfos = Group()
		for index in group:
			setattr(groupinfos,index,group[index])
		return groupinfos		

	def get_groups(self):
		result = {}
		if not self.permissions.contacts :
			return result
		data = self._get_groups()['data']
		try:
			if not data['success']:
				return result
		except KeyError:
			return result
		groups = data['result']
		self._groups = {}
		for group in groups:
			groupinfos = self._build_groupinfos(group)
			self._groups[group['id']] = groupinfos
		return self._groups
	

	def get_permissions(self):
		return self._permissions

	permissions = property(get_permissions, None, None, "freebox app permissions Permissions")
	calls       = property(get_calls, None, None, "freebox calls dict")
	groups      = property(get_groups, None, None, "freebox groups dict")
	
	uptime = property(get_uptime, None, None, "freebox uptime timedelta")
	disk_status = property(get_disk_status, None, None, "freebox disk_status string")
	fan_rpm = property(get_fan_rpm, None, None, "freebox fan rpm int")
	temp_cpub = property(get_temp_cpub, None, None, "freebox temp cpu b int")
	uptime_val = property(get_uptime_val, None, None, "freebox uptime_val int")
	board_name = property(get_board_name, None, None, "freebox board name string")
	mac = property(get_mac, None, None, "freebox mac address string")
	temp_cpum = property(get_temp_cpum, None, None, "freebox temp cpu m int")
	temp_sw = property(get_temp_sw, None, None, "freebox temp sw int")
	box_authenticated = property(get_box_authenticated, None, None, "freebox box_authenticated bool")
	serial = property(get_serial, None, None, "freebox serial string")
	firmware_version = property(get_firmware_version, None, None, "freebox firmware_version string")
	

	def __str__(self):
		fbstr = u"uptime: %s, disk_status: %s\r\nfirmware_version: %s, box_authenticated: %s\r\n"\
		% (self.uptime,self.disk_status,self.firmware_version,self.box_authenticated)
		fbstr += u"fan_rpm: %s RPM, temp_cpub: %s °C, temp_cpum: %s °C, temp_sw: %s °C\r\n"\
		% (self.fan_rpm,self.temp_cpub,self.temp_cpum,self.temp_sw)
		fbstr += u"board_name: %s, mac: %s, serial: %s"\
		% (self.board_name,self.mac,self.serial)
		return unicode(fbstr)			


class FreeboxObj(object):
	__slots__= ()
	
	def items(self):
		"dict style items"
		return [
			(field_name, getattr(self, field_name))
			for field_name in self.__slots__]

	def __iter__(self):
		"iterate over fields tuple/list style"
		for field_name in self.__slots__:
			yield getattr(self, field_name)

	def __getitem__(self, index):
		"tuple/list style getitem"
		return getattr(self, self.__slots__[index])
	
	def __str__(self):
		result = []
		for field_name in self.__slots__:
			if field_name != "__dict__":
				result.append("%s: %s" % (field_name, getattr(self,field_name)))
		return u", ".join(result)
	
	
		self._boxinfos_loaded = False
		self._uptime = timedelta(days=0) 
		self._disk_status = "" 
		self._fan_rpm = 0
		self._temp_cpub = 0
		self._uptime_val = 0 
		self._board_name = "" 
		self._mac = "" 
		self._temp_cpum = 0
		self._temp_sw = 0
		self._box_authenticated = False
		self._serial = ""
		self._firmware_version = ""
		
class Boxinfos(FreeboxObj):
	__slots__= "uptime", "disk_status", "fan_rpm", "temp_cpub", "uptime_val", "board_name", "mac",\
		"temp_cpum", "temp_sw", "box_authenticated", "serial", "firmware_version","boxinfos_loaded"

class Permissions(FreeboxObj):
	__slots__= "pvr", "explorer", "calls", "contacts", "tv", "parental", "settings", "downloader"
	
class Call(FreeboxObj):
	__slots__= "number", "type", "id", "duration", "datetime", "contact_id", "line_id", "name", "new",\
			"missed", "accepted", "outgoing"

class Contact(FreeboxObj):
	__slots__= "__dict__","first_name", "last_name", "display_name", "addresses", "notes", "company", "emails",\
			"last_update", "birthday", "numbers", "urls", "id", "photo_url"

class Group(FreeboxObj):
	__slots__= "__dict__", "nb_contact", "id", "name"
