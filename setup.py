#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cwa_qr',
    version='1.2.1',
    description='Python Implementation of the CoronaWarnApp (CWA) Event Registration',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Peter Körner',
    author_email='peter@mazdermind.de',
    url='https://github.com/MaZderMind/cwa-qr',
    project_urls={
        "Bug Tracker": "https://github.com/MaZderMind/cwa-qr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    packages=find_packages(),
    install_requires=[
        "Pillow==8.3.2",
        "protobuf==3.15.8",
        "qrcode==6.1",
        "six==1.15.0",
        "svgutils==0.3.4",
    ],
    zip_safe=True,
)
