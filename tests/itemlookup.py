import unittest, sys, pdb

# quick-n-dirty for debug only
sys.path.append('..')
import ecs
class ItemLookupTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.ItemId = "0596009259"
	
	def assertIsInteger(self, n, message=None):
		try:
			int(n)
		except :
			fail(message)
			
			
		

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
		self.assertIsInteger(book.OfferSummary.LowestNewPrice.Amount, 
			'book.OfferSummary.LowestNewPrice.Amount is not integer')

		# SalesRank
		self.assertNotEqual(book.SalesRank, '0')

	def testAccessories(self):
		# We have to use Palm Tungsten X
		txs = ecs.ItemLookup('B000BI7NHY', ResponseGroup='Accessories')
		self.assertEqual(len(txs), 1)
		tx = txs[0]
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
		
		# arbitary seller
		self.assertNotEqual(tx.Offers[23].Merchant.MerchantId, None)


	def testReviews(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Reviews')
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertEqual(len(book.CustomerReviews), 68)

		# arbitary reviewer
		self.assertEqual(book.CustomerReviews[34].Reviewer.Name, 'Sameer')
		self.assertEqual(book.CustomerReviews[12].Summary, 'An Essential Python Book for Python Programmers')


	def testSimilarities(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Similarities')
		self.assertEqual(len(books), 1)
		book = books[0]

		sim = book.SimilarProducts;
		self.assertEqual(len(sim), 5)
		self.assertEqual(sim[0].Title, 'Learning Python, Second Edition')
		self.assertEqual(sim[1].Title, 'Python Cookbook')
		self.assertEqual(sim[3].Title, "Python Essential Reference (3rd Edition) (Developer's Library)")

	def testSubjects(self):
		books = ecs.ItemLookup(self.ItemId, ResponseGroup='Subjects')
		self.assertEqual(len(books), 1)
		book = books[0]

		subs = book.Subjects;
		self.assertEqual(len(subs), 10)
		self.assertEqual(subs[0], 'Programming languages')
		self.assertEqual(subs[2], 'Computers')

	def testTracks(self):
		cds = ecs.ItemLookup('B0000042H4', ResponseGroup='Tracks')
		self.assertEqual(len(cds), 1)
		cd = cds[0].Tracks
		self.assertEqual(len(cd.Disc), 14)
		self.assertEqual(cd.Disc[13].Track[5], 'Gotterdammerung: Dritter Aufzug, Zweite Szene: Hoiho!')
		self.assertEqual(cd.Disc[4].Track[3], 'Die Walkure: Zweiter Aufzug, Funfte Szene: Zauberfest bezahmt ein Schlaf der Holden Schmerz und Harm')

	def testVariationMinimum(self):
		shirts = ecs.ItemLookup('B000EI6M5A', ResponseGroup='VariationMinimum')
		self.assertEqual(len(shirts), 1)
		shirt = shirts[0]
		self.assertEqual(shirt.Variations[0].ASIN, 'B000EG9PLU')
		self.assertEqual(shirt.Variations[5].ASIN, 'B000EG5DUM')

	def testVariationSummary(self):
		shirts = ecs.ItemLookup('B000EI6M5A', ResponseGroup='VariationSummary')
		self.assertEqual(len(shirts), 1)
		shirt = shirts[0]
		self.assertEqual(shirt.VariationSummary.HighestPrice.Amount, '699') 
		self.assertEqual(shirt.VariationSummary.LowestPrice.Amount, '699') 


	def testVariations(self):
		shirts = ecs.ItemLookup('B000EI6M5A', ResponseGroup='Variations')
		self.assertEqual(len(shirts), 1)
		shirt = shirts[0]
		self.assertEqual(shirt.Variations[0].ASIN, 'B000EG9PLU')
		self.assertEqual(shirt.Variations[5].ASIN, 'B000EG5DUM')
		self.assertEqual(shirt.VariationSummary.HighestPrice.Amount, '699') 
		self.assertEqual(shirt.VariationSummary.LowestPrice.Amount, '699') 


if __name__ == "__main__" :
	unittest.main()
