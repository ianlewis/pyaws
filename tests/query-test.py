import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class QueryTest( unittest.TestCase ):
    def testBadLicenseKey(self):
        ecs.setLicenseKey( "1MGDS69U8JF7QC7JDZG4" )
        self.assertRaises( ecs.InvalidParameterValue, ecs.query, ecs.ItemLookup( "0596002815" ) )

if __name__ == "__main__" :
    unittest.main()

