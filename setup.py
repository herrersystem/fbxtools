from setuptools import setup

setup(name = 'fbxtools',
	version = '1.1',
	author = 'herrersystem',
	author_email = 'contact@evhunter.fr',
	
	url = "http://github.com/herrersystem/fbxtools",
	keywords = 'fbx freebox',
	description = 'Provide intialisation, connect and disconnect functions for Freebox OS application.',
	license = 'GNU General Public License (GPL)',
	packages = ['fbxtools'],
	install_requires = ['apize', 'netifaces'],
	
	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
	],
)
