import unittest, sys, pdb

# quick-n-dirty for debug only
sys.path.append('..')
import ecs
class ItemLookupTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.ItemId = "0596009259"

	def testSmall(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Request,Small')
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertNotEqual(book, None)

		self.assertEqual(book.ASIN, '0596009259')
		self.assertEqual(book.Title, 'Programming Python')
		self.assertEqual(book.Manufacturer, "O'Reilly Media, Inc.")
		self.assertEqual(book.ProductGroup, 'Book')
		self.assertEqual(book.Author, 'Mark Lutz')

	def testMedium(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Request,Medium')
		self.assertEqual(len(books), 1)
		book = books[0]

		self.assertEqual(book.ASIN, '0596009259')
		self.assertEqual(book.Title, 'Programming Python')
		self.assertEqual(book.Manufacturer, "O'Reilly Media, Inc.")
		self.assertEqual(book.ProductGroup, 'Book')
		self.assertEqual(book.Author, 'Mark Lutz')

		# EditorialReview
		self.assertEqual(len(book.EditorialReviews), 2)
		self.assertEqual(book.EditorialReviews[0].Source, 'Amazon.com')
		self.assertEqual(book.EditorialReviews[1].Source, 'Book Description')

		# Images 
		self.assertEqual(len(book.ImageSets), 1)
		self.assertEqual(book.ImageSets[0].LargeImage.Height, '500')
		self.assertEqual(book.ImageSets[0].MediumImage.Height, '160')
		self.assertEqual(book.ImageSets[0].SmallImage.Height, '75')

		# ItemAttributes
		pass

		# ItemIds
		pass

		# OfferSummary
		self.assertNotEqual(book.OfferSummary.TotalNew, '0')
		self.assertEqual(book.OfferSummary.LowestNewPrice.Amount, '3420')

		# SalesRank
		self.assertNotEqual(book.SalesRank, '0')

	def testAccessories(self):
		# We have to use Palm Tungsten X
		txs = ecs.ItemLookup('B000BI7NHY', ResponseGroup='Accessories')
		self.assertEqual(len(txs), 1)
		tx = txs[0]
		self.assertEqual(len(tx.Accessories), 5)
		self.assertEqual(tx.Accessories[4].ASIN, 'B00006BB9E')

	def testBrowseNodes(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='BrowseNodes')
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertEqual(len(book.BrowseNodes), 11)
		bn = book.BrowseNodes[0]
		# iterate all the ancestors
		names = ('Perl', 'Programming', "O'Reilly", 'By Publisher')
		for x in names:
			self.assertEqual(bn.Name, x)
			bn = bn.Ancestors[0]

		self.assertEqual(bn.Name, 'Books')

	def testLarge(self):
		#books = ecs.ItemLookup(self.ItemId, ResponseGroup='Large')
		pass
	
	def testListmaniaLists(self):
		# TODO: need to find the item with this attributes
		pass

	def testOfferFull(self):
		txs = ecs.ItemLookup('B000BI7NHY', MerchantId='All', Condition='All', ResponseGroup='OfferFull')
		self.assertEqual(len(txs), 1)
		tx = txs[0]
		self.assertEqual(len(tx.Offers), 38)
		
		# arbitary seller
		self.assertEqual(tx.Offers[14].Seller.Nickname, 'tfitag') 
		self.assertEqual(tx.Offers[23].Merchant.Name, 'Technology Galaxy')


	def testReviews(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Reviews')
		self.assertEqual(len(books), 1)
		book = books[0]
		pdb.set_trace()


if __name__ == "__main__" :
	unittest.main()
