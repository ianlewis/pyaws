
import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

def dump(list):
    print "ListId: ", list.ListId
    print "CustomerName: ", list.CustomerName
    print 

class ListTest( unittest.TestCase ):
    def setUp(self):
        ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

    def testListSearch(self):
        lists = ecs.ListSearch( ListType="WishList", City="Chicago", FirstName="Sam" )
        self.assert_( len(lists) > 3 )
        list = lists[0]
        self.assertNotEqual( list, None )
        dump( list )
        self.assert_( list.CustomerName.find( "Sam" ) > -1 )


if __name__ == "__main__" :
    unittest.main()

