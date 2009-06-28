import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class SettingYourSecretAccessKeyTest( unittest.TestCase ):
    
    def setUp(self):
        ecs.SECRET_ACCESS_KEY = None

    def testGetSecretAccessKey(self):
        self.assertRaises( ecs.NoSecretAccessKey, ecs.getSecretAccessKey )

    def testSetSecretAccessKey(self):
        self.assertRaises( ecs.NoSecretAccessKey, ecs.setSecretAccessKey )

    def testSetSecretKeyFromEnv(self):
        import os
        os.environ['AWS_SECRET_ACCESS_KEY'] = "FAKE-KEY"
        self.assertEqual( ecs.getSecretAccessKey(), "FAKE-KEY" )
        
    def testSetSecretKey(self):
        ecs.setSecretAccessKey('1234')
        self.assertEqual(ecs.getSecretAccessKey(), '1234')
        
class AuthenticationTest(unittest.TestCase):
    def testBuildTheSignature(self):
        '''example taken from the api-documentation'''
        netloc = 'webservices.amazon.com'
        query = 'AWSAccessKeyId=00000000000000000000&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=ItemAttributes%2COffers%2CImages%2CReviews&Service=AWSECommerceService&Timestamp=2009-01-01T12%3A00%3A00Z&Version=2009-01-06'
        expected_signature = 'Nace%2BU3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg%3D'
        self.assertEqual(ecs.buildSignature(netloc, query),expected_signature)
                
    def testBuildQuery(self):
        '''example taken from the api-documentation'''
        ecs.setSecretAccessKey('1234567890')
        
        args = {
                'Service':'AWSECommerceService',
                'AWSAccessKeyId':'00000000000000000000',
                'Timestamp':'2009-01-01T12:00:00Z',
                'Operation':'CartCreate',
                'Item.1.OfferListingId':'j8ejq9wxDfSYWf2OCp6XQGDsVrWhl08GSQ9m5j+e8MS449BN1XGUC3DfU5Zw4nt/FBt87cspLow1QXzfvZpvzg==',
                'Item.1.Quantity':'3',
                'AssociateTag':'mytag-20',
                'Version':'2009-01-01'
        }
        expepected_url = 'http://ecs.amazonaws.com/onca/xml?AWSAccessKeyId=00000000000000000000&AssociateTag=mytag-20&Item.1.OfferListingId=j8ejq9wxDfSYWf2OCp6XQGDsVrWhl08GSQ9m5j%2Be8MS449BN1XGUC3DfU5Zw4nt%2FFBt87cspLow1QXzfvZpvzg%3D%3D&Item.1.Quantity=3&Operation=CartCreate&Service=AWSECommerceService&Timestamp=2009-01-01T12%3A00%3A00Z&Version=2009-01-01&Signature=cF3UtjbJb1%2BxDh387C%2FEmS1BCtS%2FZ01taykBCGemvUU%3D'
        self.assertEqual(ecs.buildQuery(args),expepected_url)

if __name__ == "__main__" :
    unittest.main()

