import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class QueryTest( unittest.TestCase ):
    def testBadLicenseKey(self):
        ecs.setLicenseKey( "1MGVS72Y8JF7EC7JDZG0" )
        self.assertRaises( ecs.InvalidParameterValue, ecs.ItemLookup, "0596002818" )


if __name__ == "__main__" :
    unittest.main()

