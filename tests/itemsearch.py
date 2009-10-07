import unittest, sys, pdb
import re

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

def test_suite():
    from unittest import defaultTestLoader as loader
    return loader.loadTestsFromName("tests.itemsearch")

class ItemSearchTest(unittest.TestCase):

	def assertIsInteger(self, n, message=None):
		try:
			int(n)
		except :
			fail(message)

	def assertRequest(self, n):
		self.assertTrue(hasattr(n, "Request"))
		self.assertTrue(n.Request.isValid)
	
	def assertAccessories(self, n):
		self.assertTrue(hasattr(n, "Accessories"))
		for a in n.Accessories:
			self.assertTrue(hasattr(a, "ASIN"))
			self.assertTrue(hasattr(a, "Title"))
	
	def assertBrowseNode(self, n):
		self.assertTrue(hasattr(n, "BrowseNodes"))
		for b in n.BrowseNodes:
			self.assertTrue(hasattr(b, "BrowseNodeId"))
			self.assertTrue(hasattr(b, "Name"))

	def assertMedium(self, n):
		self.assertSmall(n)
		#self.assertRequest(n)
	
	def assertSmall(self, n):
		self.assertTrue(hasattr(n, "ASIN"))
		self.assertTrue(hasattr(n, "Title"))
		self.assertTrue(hasattr(n, "ProductGroup"))
			
	def testSmall(self):
		books = ecs.ItemSearch("XML Python", SearchIndex="Books", ResponseGroup='Request,Small')
		for i in range(10):
			self.assertSmall(books[i])

	def testMedium(self):
		books = ecs.ItemSearch("XML Python", SearchIndex="Books", ResponseGroup='Request,Medium')
		for i in range(10):
			self.assertMedium(books[i])

	def testAccessories(self):
		# We have to use Palm Tungsten X
		txs = ecs.ItemSearch('Zen', SearchIndex='Electronics', ResponseGroup='Small,Accessories')
		for i in range(10):
			self.assertAccessories(txs[i])

	def testBrowseNodes(self):
		books = ecs.ItemSearch('XML Python', SearchIndex='Books', ResponseGroup='BrowseNodes')
		for i in range(10):
			self.assertBrowseNode(books[i])

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
