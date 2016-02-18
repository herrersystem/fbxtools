# Fbxtools

Interface within Freebox OS API and Python

### Installation

```
pip install fbxtools
```


### Compatibility

* Freebox OS API v2, v3
* Python 3.x

### Documentation

https://pythonhosted.org/fbxtools/index.html

### Example

Create file __app_details.json__:
```
{
"app_id": "fr.freebox.testapp",
"app_name":"testapp",
"app_version":"0.0.1",
"device_name":"my_pc"
}
```

example for get call log:

```
import os
import fbxtools.fbxtools as fbxtools
import fbxtools.calls as calls

if os.path.isfile('app_token.json'):
	app=fbxtools.connect_app()
		
	if app != False:
		result=calls.get_call_log(app)
		print(result)
		
		if result == False:
			print(app.get_last_err())
		
		fbxtools.deconnect_app(app)
else:
	#First execution:
	#Authorize the application by pressing '>' on the Freebox screen.
	fbxtools.init_app()
	#After that, reload manually your app.

```
