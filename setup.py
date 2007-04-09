from distutils.core import setup
from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None


setup(name='pyaws',
	version='0.2.0',
	package_dir={'pyaws': ''},
	packages=['pyaws'],
	author='Kun Xi',
	author_email='kunxi@kunxi.org', 
	description='A Python wrapper for Amazon Web Service',
	long_description='PyAWS is a Python wrapper for the latest Amazon Web Service. It is designed to pave the way for Python developers to interactivate AWS. This project is forked from the code base of pyamazon. The Amazone E-Commerce Services is supported.', 
	url='http://pyaws.sourceforge.net',
	license='Python Software Foundation License',
	platforms='OS Independent',
	download_url='http://prdownloads.sourceforge.net/pyaws/pyaws-0.1.0.tar.gz?download',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Python Software Foundation License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: WWW/HTTP',
          ]
)
