# Fbxtools

Provide intialisation, connect and disconnect functions for Freebox OS application.

## Installation

```bash
pip install fbxtools
```

## Get started

### Fbx class

```
from fbxtools.fbx import Fbx
```

Accept 3 arguments:
* url (__str__) : Freebox OS API url's
* app_infos (__str__) : filepath of app_infos file (default: 'app_infos.json') 
* app_auth (__str__) : filepath of app_auth file (default: 'app_auth.json')
* verify_cert (__bool__ or __str__) : disable SSL cert verification or get certfile path. (default True)

### app_infos.json file

This file provide application informations. Must be created manually.

See http://dev.freebox.fr/sdk/os/login/#tokenrequest-object 

example :
```json
{
	"app_id": "fr.freebox.test",
	"app_name": "test",
	"app_version": "0.0.1",
	"device_name": "mycomputer"
}
```

### app_auth.json file:

This file provide connect informations. Automatically generated with Fbx.get_app_token().

See http://dev.freebox.fr/sdk/os/login/#tokenrequest-object

example : 
```json
{
	"track_id": 6, 
	"app_token": "vfItuATAq8luiuDmo3ZeVVhb0Cv9uImxN2/VJRLa1rOjUsjkBxbEgPY9VwiwpSxq"
}
```

### First use (Init app)

```python
from fbxtools.fbx import Fbx

app = Fbx('http://mafreebox.freebox.fr/api/v3')
appToken, trackId = app.get_app_token()
print('[fbx] Press ">" on the dial of the Freebox')

## Optionnaly, you can verify your authorization status for your app.
import time

currentStatus = ''
attempt = 5
while attempt > 0:
	time.sleep(3)
	response = app.track_auth_progress(trackId)
	if response['data']['success']:
		currentStatus = response['data']['result']['status']
	if currentStatus == 'granted':
		print('[fbx] Your application got authorization !')
		break
	print('[fbx] attempts remaining: ' + str(attempt) + 
		', status: ' + currentStatus)
	attempt -= 1
app.disconnect_app()
```

This function generated automatically 'app_auth.json' file. For Fbx.url argument, you can use:
* generic url http://mafreebox.freebox.fr
* get reel url with fbxtools.utils.get_url_api().

example :
```python
from fbxtools.utils import get_url_api
from fbxtools.fbx import Fbx

url_api = get_url_api()
app = Fbx(url_api)
app.get_app_token()
```

Use this if you are on the __same network__ as your freebox.

### Call API.
```python
from fbxtools.fbx import Fbx

app = Fbx('http://mafreebox.freebox.fr/api/v3')
app.get_session_token()


@app.api.call('/lcd/config')
def get_config():
	'''
	http://dev.freebox.fr/sdk/os/lcd/#get-the-current-lcd-configuration
	''' 
	return {}


@app.api.call('/lcd/config', method='PUT')
def update_config(config):
	'''
	http://dev.freebox.fr/sdk/os/lcd/#update-the-lcd-configuration
	'''
	return {'data': config, 'is_json': True}


new_config = {	
	"brightness": 50,
	"orientation": 90,
	"orientation_forced": False
}

resp = get_config()
app.disconnect_app()
print(resp)
```

