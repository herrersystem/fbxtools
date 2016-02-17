#!/usr/bin/env python


class Application:
	def __init__(self):
		self.session_token='' #App identification.
		self.name='' #App configuration.
		self.id=''
		self.version=''
		
		self.api_version=''
		self.api_base_url=''

		self.AUTH_SETTINGS=False
		self.AUTH_EXPLORER=False
		self.AUTH_TV=False
		self.AUTH_PVR=False
		self.AUTH_PARENTAL=False
		self.AUTH_DOWNLOADER=False
		self.AUTH_CONTACTS=False
		self.AUTH_CALLS=False
		
		self.err_log=list()
		
	def __str__(self):
		return self.name
	
	def set_permission(self, permission):
		'''
		Obtains permissions of app.
		'''
		if permission['settings']:
			self.AUTH_SETTINGS=True
		if permission['explorer']:
			self.AUTH_EXPLORER=True
		if permission['tv']:
			self.AUTH_TV=True
		if permission['pvr']:
			self.AUTH_PVR=True
		if permission['parental']:
			self.AUTH_PARENTAL=True
		if permission['downloader']:
			self.AUTH_DOWNLOADER=True
		if permission['contacts']:
			self.AUTH_CONTACTS=True
		if permission['calls']:
			self.AUTH_CALLS=True	
		
		return 0
	
	def get_last_err(self):
		if len(self.err_log) > 0:
			return self.err_log[-1]
		
		return []
