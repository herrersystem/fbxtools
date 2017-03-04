#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import print_function

from datetime import timedelta, datetime
from fbxtools.fbx import *

class FreeboxObj(object):

	_url_get = ''

	def __init__(self, fbx=None, data=None, attribs={'id': {}}):
		self._attribs = attribs
		self._fbx = None
		if fbx != None:
			self._fbx = fbx
		if data != None:			
			self.load_data(data)
			
	def load_data(self, data):
		if isinstance(data, dict):
			for field_name in self._attribs:
				if field_name in data:
					if isinstance(data[field_name],list):
						obj_list = []
						for elem in data[field_name]:
							infos = None
							if self._attribs[field_name]['type_info'] == "Address":
								infos = Address(data=elem)
							elif self._attribs[field_name]['type_info'] == "Number":
								infos = Number(data=elem)
							elif self._attribs[field_name]['type_info'] == "Email":
								infos = Email(data=elem)
							elif self._attribs[field_name]['type_info'] == "Url":
								infos = Url(data=elem)	
							elif self._attribs[field_name]['type_info'] == "Contact":
								infos = Contact(data=elem)	
							elif self._attribs[field_name]['type_info'] == "Call":
								infos = Call(data=elem)	
							elif self._attribs[field_name]['type_info'] == "Contacts":
								infos = Contacts(data=elem)	
							if infos != None:						
								obj_list.append(infos)
						setattr(self, field_name, obj_list)
					else:
						if self._attribs[field_name]['type_info'] == datetime:
							setattr(self, field_name, datetime.fromtimestamp(data[field_name]))
							#setattr(self, field_name, data[field_name])
						else:
							setattr(self, field_name, data[field_name])
		elif isinstance(data, FreeboxObj):
			for field_name in self._attribs:
				try:
					setattr(self, field_name, getattr(data,field_name))
				except AttributeError:
					pass
		elif isinstance(data, list):
			# Quel est le type de data ?
			fbxobj_type = "Contacts"
			for field_name in self._attribs:
				print(field_name)
				if self._attribs[field_name]['type_info'] == "Contact":
					fbxobj_type = "Contacts"
					break
				elif self._attribs[field_name]['type_info'] == "Call":
					fbxobj_type = "Calls"
					break
			obj_list = []
			for elem in data:
				if fbxobj_type == "Contacts":
					infos = Contact(data=elem)
				elif fbxobj_type == "Calls":
					infos = Call(data=elem)
				obj_list.append(infos)
			if fbxobj_type == "Contacts":
				setattr(self, 'contacts', obj_list)
			elif fbxobj_type == "Calls":
				setattr(self, 'calls', obj_list)
					
	def _get_by_id(self,url,id=None,contact_id=None,data=None):
		@self._fbx.api.call(url)
		def wrapper():
			if data != None:
				args = {'args': data, 'is_json': True}
				return {'args': args}
			if id != None:
				if contact_id == None :
					args = {'id': id}
				else:
					args = {'id': id, 'contact_id': contact_id}
				return {'args': args}
			else:
				return {}

		return wrapper()
					
	def get_by_id(self,id=None,contact_id=None,data=None):
		if self._fbx == None :
			print('get_by_id',self.__class__,id,contact_id)
			return self
		if id == None:
			datar = self._get_by_id(self._url_get,data=data)['data']
		else:
			datar = self._get_by_id(self._url_get+':id',id,data=data)['data']
		#print(datar)
		try:
			if not datar['success']:
				return self
		except KeyError:
			return self
		result = datar['result']
		self.load_data(result)
		return self
					
	def _set_by_id(self,url,id,data):
		@self._fbx.api.call(url, method='PUT')
		def wrapper():
			if id != None:
				args = {'id': id}
				print(args)
				print(data)
				return {'args': args, 'data': data, 'is_json': True}
			else:
				return {}

		return wrapper()
					
	def set_by_id(self,id,params):
		if isinstance(params, FreeboxObj):
			datadict = params.fbobj2dict()
		else:
			datadict = params
		respons = self._set_by_id(self._url_get+':id',id,params)
		print(respons)
		data = respons['data']
		try:
			if not data['success']:
				return self
		except KeyError:
			return self
		result = data['result']
		infos = self.load_data(result)
		return infos
					
	def _new_fbxobj(self,url,data):
		@self._fbx.api.call(url, method='POST')
		def wrapper():
			return {'data': data, 'is_json': True}

		return wrapper()
					
	def new_fbxobj(self,params):
		if isinstance(params, FreeboxObj):
			datadict = params.fbobj2dict()
		else:
			datadict = params
		print(datadict)
		respons = self._new_fbxobj(self._url_get,datadict)
		print(respons)
		data = respons['data']
		try:
			if not data['success']:
				return self
		except KeyError:
			return self
		result = data['result']
		self.load_data(result)
		return self
					
	def _delete_by_id(self,url,id):
		@self._fbx.api.call(url, method='DELETE')
		def wrapper():
			args = {'id': id}
			return {'args': args}

		return wrapper()
					
	def delete_by_id(self,id):
		respons = self._delete_by_id(self._url_get+':id',id)
		print(respons)
		

	def __str__(self):
		result = ["\r\n"]
		for field_name in self._attribs:
			if field_name != "__dict__":
				try:
					datas = getattr(self,field_name)
					if isinstance(datas,list):
						#print(unicode(datas))
						#result.append("\r\n%s:" % (field_name))
						for data in datas:
							result.append("\t%s:%s\r\n" % (field_name,data))
					else:
						#st = datetime.fromtimestamp(result['datetime']).strftime('%Y-%m-%d %H:%M:%S')
						if self._attribs[field_name]['type_info'] == datetime:
							#result.append("%s: '%s'" % (field_name, datas.strftime('%Y-%m-%d %H:%M:%S')))
							result.append("%s: '%s'" % (field_name, datas))
						else:
							result.append("%s: '%s'" % (field_name, datas))
				except:
					pass
		return u"\r\n".join(result)
	
	def fbobj2dict(self):
		result = {}
		for field_name in self._attribs:
			if field_name != "__dict__":
				try:
					if getattr(self,field_name) != None:
						result[field_name] = getattr(self,field_name)
				except:
					pass
		return result
	
class Boxinfos(FreeboxObj):
	
		def __init__(self, fbx=None, data={}, attribs={\
			'uptime':       {'list': False,'type_info': str},\
			'disk_status':  {'list': False,'type_info': bool},\
			'fan_rpm':      {'list': False,'type_info': int},\
			'temp_cpub':    {'list': False,'type_info': int},\
			'uptime_val':   {'list': False,'type_info': timedelta},\
			'board_name':        {'list': False,'type_info': str},\
			'mac':               {'list': False,'type_info': str},\
			'temp_cpum':         {'list': False,'type_info': int},\
			'temp_sw':           {'list': False,'type_info': int},\
			'box_authenticated': {'list': False,'type_info': bool},\
			'serial':            {'list': False,'type_info': str},\
			'firmware_version':  {'list': False,'type_info': str},\
			'boxinfos_loaded':   {'list': False,'type_info': bool}\
		}):
			FreeboxObj.__init__(self, fbx, data, attribs)

class Permissions(FreeboxObj):
	
		def __init__(self, fbx=None, data={}, attribs={\
			'pvr':      {'list': False,'type_info': bool},\
			'explorer': {'list': False,'type_info': bool},\
			'calls':    {'list': False,'type_info': bool},\
			'contacts': {'list': False,'type_info': bool},\
			'tv':       {'list': False,'type_info': bool},\
			'parental': {'list': False,'type_info': bool},\
			'settings': {'list': False,'type_info': bool},\
			'downloader': {'list': False,'type_info': bool}\
		}):
			FreeboxObj.__init__(self, fbx, data, attribs)

class Calls(FreeboxObj):
	
	_url_get = '/call/log/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'calls':   {'list': True,'type_info': "Call"}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)
	
class Call(FreeboxObj):
	
	_url_get = '/call/log/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'number':     {'list': False,'type_info': str},\
		'type':       {'list': False,'type_info': str},\
		'id':         {'list': False,'type_info': int},\
		'duration':   {'list': False,'type_info': timedelta},\
		'datetime':   {'list': False,'type_info': datetime},\
		'contact_id': {'list': False,'type_info': int},\
		'line_id':    {'list': False,'type_info': int},\
		'name':       {'list': False,'type_info': str},\
		'new':        {'list': False,'type_info': bool},\
		'missed':     {'list': False,'type_info': bool},\
		'accepted':   {'list': False,'type_info': bool},\
		'outgoing':   {'list': False,'type_info': bool}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)

class Contacts(FreeboxObj):
	
	_url_get = '/contact/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'contacts':   {'list': True,'type_info': "Contact"}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)

class Contact(FreeboxObj):
	
	_url_get = '/contact/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'first_name':   {'list': False,'type_info': str},\
		'last_name':    {'list': False,'type_info': str},\
		'display_name': {'list': False,'type_info': str},\
		'addresses':    {'list': True,'type_info': "Address"},\
		'notes':        {'list': False,'type_info': str},\
		'company':      {'list': False,'type_info': str},\
		'emails':       {'list': False,'type_info': "Email"},\
		'last_update':  {'list': False,'type_info': datetime},\
		'birthday':     {'list': False,'type_info': str},\
		'numbers':      {'list': True,'type_info': "Number"},\
		'urls':         {'list': True,'type_info': "Url"},\
		'id':           {'list': False,'type_info': int},\
		'photo_url':    {'list': False,'type_info': str}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)

class Group(FreeboxObj):
	
	def __init__(self, fbx=None, data={}, attribs={\
		'nb_contact': {'list': False,'type_info': int},\
		'id':         {'list': False,'type_info': int},\
		'name':       {'list': False,'type_info': str}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)

class Number(FreeboxObj):
	
	_url_get = '/number/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'number':     {'list': False,'type_info': int},\
		'contact_id': {'list': False,'type_info': int},\
		'is_default': {'list': False,'type_info': bool},\
		'is_own':     {'list': False,'type_info': bool},\
		'type':       {'list': False,'type_info': str},\
		'id':         {'list': False,'type_info': int}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)
		try:
			if (self._fbx) \
			and (self.contact_id)\
			and (self.number):
				self.new_fbxobj(self)
		except AttributeError:
			pass


class Address(FreeboxObj):
	
	_url_get = '/address/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'city':       {'list': False,'type_info': str},\
		'country':    {'list': False,'type_info': str},\
		'street2':    {'list': False,'type_info': str},\
		'zipcode':    {'list': False,'type_info': str},\
		'contact_id': {'list': False,'type_info': int},\
		'number':     {'list': False,'type_info': int},\
		'street':     {'list': False,'type_info': str},\
		'type':       {'list': False,'type_info': str},\
		'id':         {'list': False,'type_info': int}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)
		try:
			if (self._fbx) \
			and (self.contact_id):
				self.new_fbxobj(self)
		except AttributeError:
			pass

class Email(FreeboxObj):
	
	_url_get = '/email/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'email':      {'list': False,'type_info': str},\
		'contact_id': {'list': False,'type_info': int},\
		'type':       {'list': False,'type_info': str},\
		'id':         {'list': False,'type_info': int}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)
		try:
			if (self._fbx) \
			and (self.contact_id)\
			and (self.email):
				self.new_fbxobj(self)
		except AttributeError:
			pass

class Url(FreeboxObj):
	
	_url_get = '/url/'
	
	def __init__(self, fbx=None, data={}, attribs={\
		'url':        {'list': False,'type_info': str},\
		'contact_id': {'list': False,'type_info': int},\
		'type':       {'list': False,'type_info': str},\
		'id':         {'list': False,'type_info': int}\
	}):
		FreeboxObj.__init__(self, fbx, data, attribs)
		try:
			if (self._fbx) \
			and (self.contact_id)\
			and (self.url):
				self.new_fbxobj(self)
		except AttributeError:
			pass
	
