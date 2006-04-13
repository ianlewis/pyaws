import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class QueryTest( unittest.TestCase ):
    def testBadLicenseKey(self):
        ecs.setLicenseKey( "1MGDS69U8JF7QC7JDZG4" )
        self.assertRaises( ecs.InvalidParameterValue, ecs.query, ecs.ItemLookup( "0596002815" ) )

    def testExceptionMessage(self):
        ecs.setLicenseKey( "1MGDS69U8JF7QC7JDZG4" )
        try:
            ecs.query( ecs.ItemLookup( "0596002815" ) )
        except ecs.InvalidParameterValue, e:
            print e.args
            self.assertNotEqual( e.args, None )
        

if __name__ == "__main__" :
    unittest.main()

