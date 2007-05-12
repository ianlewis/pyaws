import unittest, sys, pdb

# quick-n-dirty for debug only
sys.path.append('..')
import ecs
class ItemSearchTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def assertIsInteger(self, n, message=None):
		try:
			int(n)
		except :
			fail(message)
			
	def testSmall(self):
		books = ecs.ItemSearch("XML,Python", SearchIndex="Books", ResponseGroup='Request,Small')
		self.assertEqual(len(books), 7)
		titles = [u"Web Standards Programmer's Reference : HTML, CSS, JavaScript, Perl, Python, and PHP", u'Python & XML', u'XML Processing with Perl, Python, and PHP', u'Professional Linux Programming', u'XML Processing with Python (with CD-ROM)', u'Xml Processing with Python', u'Xml and Python: Web Development on the Edge']
		for i, x in enumerate(titles):
			self.assertEqual(books[i].Title, titles[i])


	def testMedium(self):
		books = ecs.ItemSearch("XML,Python", SearchIndex="Books", ResponseGroup='Request,Medium')
		self.assertEqual(len(books), 7)
		titles = [u"Web Standards Programmer's Reference : HTML, CSS, JavaScript, Perl, Python, and PHP", u'Python & XML', u'XML Processing with Perl, Python, and PHP', u'Professional Linux Programming', u'XML Processing with Python (with CD-ROM)', u'Xml Processing with Python', u'Xml and Python: Web Development on the Edge']
		for i, x in enumerate(titles):
			self.assertEqual(books[i].Title, titles[i])
		book = books[0]

		# EditorialReview
		self.assertEqual(len(book.EditorialReviews), 1)
		self.assertEqual(book.EditorialReviews[0].Source, 'Book Description')

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
		self.assertIsInteger(book.OfferSummary.LowestNewPrice.Amount)

		# SalesRank
		self.assertNotEqual(book.SalesRank, '0')

	def testAccessories(self):
		# We have to use Palm Tungsten X
		txs = ecs.ItemSearch('Zen', SearchIndex='Electronics', ResponseGroup='Small,Accessories')
		self.assert_(len(txs) >= 1)
		tx = txs[0]
		self.assertEqual(len(tx.Accessories), 5)
		self.assertEqual(tx.Accessories[4].Title, 'Sennheiser CX300-B Earbuds (Black)')

	def testBrowseNodes(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', ResponseGroup='BrowseNodes')
		self.assert_(len(books) > 1)
		book = books[0]
		self.assertEqual(book.ASIN, '0764588206')
		bn = book.BrowseNodes[0]
		# iterate all the ancestors
		names= ('JavaScript', 'Scripting & Programming', 'Web Development', 'Computers & Internet', 'Subjects')

		for x in names:
			self.assertEqual(bn.Name, x)
			bn = bn.Ancestors[0]

		self.assertEqual(bn.Name, 'Books')

	def testLarge(self):
		# TODO: find Large
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', ResponseGroup='Large')
		pass
	
	def testListmaniaLists(self):
		# TODO: need to find the item with this attributes
		pass

	def testOfferFull(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', MerchantId='All', ResponseGroup='OfferFull')
		book = books[0]
		self.assert_(len(book.Offers) > 10)
		
		# arbitary seller
		self.assertEqual(book.Offers[14].Seller.Nickname, 'a1books-com')
		self.assertEqual(book.Offers[23].Seller.SellerId, 'A1CJM7P9NE7RE7')

	def testReviews(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', MerchantId='All', ResponseGroup='Reviews')
		book = books[4]
		self.assert_(len(book.CustomerReviews) > 10)

		# arbitary reviewer
		self.assertEqual(book.CustomerReviews[3].Reviewer.Name, 'M. Bennett') 
		self.assertEqual(book.CustomerReviews[10].Summary, 'Nice followup')


	def testSimilarities(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', MerchantId='All', ResponseGroup='Similarities')
		book = books[0]

		sim = book.SimilarProducts;
		self.assertEqual(len(sim), 5)
		self.assertEqual(sim[0].Title, 'Professional JavaScript for Web Developers (Wrox Professional Guides)')
		self.assertEqual(sim[1].Title, 'Professional Ajax, 2nd Edition (Programmer to Programmer)')
		self.assertEqual(sim[3].Title, 'Ajax in Action')

	def testSubjects(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', MerchantId='All', ResponseGroup='Subjects')
		book = books[0]

		subs = book.Subjects;
		self.assert_('HTML' in subs)
		self.assert_('Computers' in subs)
		self.assert_('Programming Languages - Perl' in subs)

	def testTracks(self):
		cds = ecs.ItemSearch('Gotterdammerung', SearchIndex='Classical', ResponseGroup='Tracks')
		cd = cds[1].Tracks
		self.assertEqual(len(cd.Disc), 2)
		self.assertEqual(cd.Disc[0].Track[5], 'The Rheingold: Journey Down To Nibelheim')
		self.assertEqual(cd.Disc[1].Track[3], 'Parsifal: Good Friday Music')

	def testVariationMinimum(self):
		pass

	def testVariationSummary(self):
		pass

	def testVariations(self):
		pass


if __name__ == "__main__" :
	unittest.main()
