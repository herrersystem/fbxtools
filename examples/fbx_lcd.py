#!/usr/bin/env python

from fbxtools.fbx import Fbx

## Initialize and connect app.
app = Fbx()
app.get_session_token()


@app.api.call('/lcd/config')
def get_config():
	'''
	GET /api/v3/lcd/config/
	''' 
	return {}


@app.api.call('/lcd/config', method='PUT')
def update_config(config):
	'''
	PUT /api/v3/lcd/config/
	'''
	return {'data': config, 'is_json': True}


if __name__ == "__main__":
	new_config = {	
		"brightness": 50,
		"orientation": 90,
		"orientation_forced": False
	}

	resp = update_config(new_config)
	print(resp)
