from distutils.core import setup
from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None


setup(name='pyaws',
	version='0.1.0',
	package_dir={'pyaws': ''},
	packages=['pyaws'],
	author='Kun Xi',
	author_email='quinnxi@gmail.com', 
	description='A Python wrapper for Amazon Web Service',
	download_url='http://downloads.sourceforge.net/pyaws/pyaws-0.1.0.tar.gz?use_mirror=osdn',
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
