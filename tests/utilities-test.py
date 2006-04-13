import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class UtilitiesTest( unittest.TestCase ):
    def testDefaultLocale(self):
        self.assertEqual( ecs.getLocale(), "us" )

    def testSetLocale(self):
        ecs.setLocale( "fr" )
        self.assertEqual( ecs.getLocale(), "fr" )

    def testBadLocale(self):
        self.assertRaises( ecs.BadLocale, ecs.setLocale, "zh" )

    def testNoLicenseKey(self):
        self.assertRaises( ecs.NoLicenseKey, ecs.setLicenseKey )

if __name__ == "__main__" :
    unittest.main()
