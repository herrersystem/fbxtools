#!/usr/bin/env python

import json


def parse_auth_file(app_auth):
	with open(app_auth, 'r') as f:    
		auth = json.load(f)

	return auth


def parse_infos_file(app_infos):
	with open(app_infos, 'r') as f:    
		infos = json.load(f)

	return infos


def get_url_api():
	import netifaces
	from apize.decorators import apize_raw

	gateways = netifaces.gateways()
	fbx_ip = gateways['default'][netifaces.AF_INET][0]

	@apize_raw('http://' + fbx_ip + '/api_version')
	def get_api_config():
		return {}

	config = get_api_config()
	api_version = 'v' + config['data']['api_version'].split('.')[0]
	api_scheme = 'http://'
	api_port = ''

	if config['data']['https_available']:
		api_port = ':' + str(config['data']['https_port'])
		api_scheme = 'https://'

	api_url = '{}{}{}{}{}'.format(
		api_scheme,
		config['data']['api_domain'],
		api_port,
		config['data']['api_base_url'],
		api_version,
	)

	return api_url
