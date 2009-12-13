#!/usr/bin/env python
#:coding=utf-8:

import sys

if sys.version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None

METADATA = dict(
	name='pyaws',
	version='0.2.2',
	package_dir={'pyaws': ''},
	packages=['pyaws'],
	author='Kun Xi',
	author_email='kunxi@kunxi.org', 
	description='A Python wrapper for Amazon Web Service',
	long_description='PyAWS is a Python wrapper for the latest Amazon Web Service. It is designed to pave the way for Python developers to interactivate AWS. This project is forked from the code base of pyamazon. The Amazone E-Commerce Services is supported.', 
	url='http://pyaws.sourceforge.net',
	license='Python Software Foundation License',
	platforms='OS Independent',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Python Software Foundation License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
          ]
)

SETUPTOOLS_METADATA = dict(
	test_suite='tests',	
)

def main():
	# Use setuptools if available, otherwise fallback and use distutils
	try:
		import setuptools
		METADATA.update(SETUPTOOLS_METADATA)
		setuptools.setup(**METADATA)
	except ImportError:
		import distutils.core
		distutils.core.setup(**METADATA)

if __name__ == '__main__':
	main()
