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

if __name__ == "__main__" :
    unittest.main()

