from setuptools import setup

setup(name='fbxtools',
	version='0.2',
	author='herrersystem',
	author_email='herrersystem@mailoo.org',
	
	url="http://github.com/herrersystem/fbxtools",
	keywords='fbx freebox',
	description='interface within Python and Freebox OS API.',
	license='MIT',
	packages=["fbxtools"],
	install_requires=['requests'],
	
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
	],
)
