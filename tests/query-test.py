import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

def dump(book):
    print "ASIN: ", book.ASIN
    print "Title : ", book.Title
    print "Author: ", book.Author
    print "Manufacturer: ", book.Manufacturer
    print 

class QueryTest( unittest.TestCase ):
    def setUp(self):
        ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

    def testItemLookup(self):
        books = ecs.ItemLookup("0596009259")
        self.assertEqual( len(books), 1 )
        book = books[0]
        self.assertNotEqual( book, None )

        self.assertEqual( book.ASIN, u'0596009259' )
        self.assertEqual( book.Title, u'Programming Python' )
        self.assertEqual( book.Manufacturer, u"O'Reilly Media" )
        self.assertEqual( book.ProductGroup, u'Book' )
        self.assertEqual( book.Author, u'Mark Lutz')


    def testItemSearch(self):
        books = ecs.ItemSearch("python", SearchIndex="Books")
        self.assert_( len(books) > 200, "We are expect more than 200 books are returned." )
        self.assertNotEqual( books[100], None )
    
    def testSimilarityLookup(self):
        books = ecs.SimilarityLookup("0596009259")
        for book in books:
            dump( book )
        self.assert_( len(books) > 9, "We are expect more than 9 books are returned." )

if __name__ == "__main__" :
    unittest.main()

