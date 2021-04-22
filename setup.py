#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
	name='cwa',
	version='1.0',
	description='Python Implementation of the CoronaWarnApp (CWA) Event Registration',
	author='Greg Ward',
	author_email='github@mazdermind.de',
	url='https://github.com/MaZderMind/cwa-qr',
	packages=find_packages(),
	install_requires=[
		"Pillow==8.2.0",
		"protobuf==3.15.8",
		"qrcode==6.1",
		"six==1.15.0",
	],
	zip_safe=True,
)
