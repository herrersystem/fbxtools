#!/usr/bin/env python

class Application:
	def __init__(self):
		self.session_token='' #App identification.
		self.name='' #App configuration.
		self.id=''
		self.version=''
		
		self.api_version=float()
		self.api_base_url='/api/v'

		self.AUTH_SETTINGS=False
		self.AUTH_EXPLORER=False
		self.AUTH_TV=False
		self.AUTH_PVR=False
		self.AUTH_PARENTAL=False
		self.AUTH_DOWNLOADER=False
		self.AUTH_CONTACTS=False
		self.AUTH_CALLS=False
	
	def __str__(self):
		return self.name
