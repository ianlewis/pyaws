import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class LicenseKeyTest( unittest.TestCase ):

	def testGetLicenseKey(self):
		self.assertRaises( ecs.NoLicenseKey, ecs.getLicenseKey )

	def testSetLicenseKey(self):
		self.assertRaises( ecs.NoLicenseKey, ecs.setLicenseKey )

	def testSetLicenseKeyFromEnv(self):
		import os
		os.environ['AWS_LICENSE_KEY'] = "FAKE-KEY"
		self.assertEqual( ecs.getLicenseKey(), "FAKE-KEY" )

class LicenseTestSuite(unittest.TestSuite):
	# Add suite here since order matters 
	def __init__(self):
		unittest.TestSuite.__init__(self, map(LicenseKeyTest, 
			('testGetLicenseKey', 'testSetLicenseKey', 'testSetLicenseKeyFromEnv')))


if __name__ == "__main__" :
	unittest.main()

