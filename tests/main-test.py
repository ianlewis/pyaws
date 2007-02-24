import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class ListTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, list):
		print "ListId: ", list.ListId
		print "CustomerName: ", list.CustomerName
		print 

	def testListSearch(self):
		lists = ecs.ListSearch(ListType="WishList", City="Chicago", FirstName="Sam")
		self.assert_(len(lists) > 3)
		list = lists[0]
		self.assertNotEqual(list, None)
		self.dump(list)
		self.assert_(list.CustomerName.find("Sam") > -1)

	def testListLookup(self):
		lists = ecs.ListLookup(ListType="WishList", ListId="13T2CWMCYJI9R")
		self.assertNotEqual(lists, None)
		self.assertEqual(lists[0].CustomerName, "Sam")

class QueryTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, book):
		try:
			print "ASIN: ", book.ASIN
			print "Title : ", book.Title
			print "Author: ", book.Author
			print "Manufacturer: ", book.Manufacturer
			print 
		except :
			pass

	def testItemLookup(self):
		books = ecs.ItemLookup("0596009259")
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertNotEqual(book, None)

		self.assertEqual(book.ASIN, u'0596009259')
		self.assertEqual(book.ItemAttributes.Title, u'Programming Python')
		self.assertEqual(book.ItemAttributes.Manufacturer, u"O'Reilly Media")
		self.assertEqual(book.ItemAttributes.ProductGroup, u'Book')
		self.assertEqual(book.ItemAttributes.Author, u'Mark Lutz')


	def testItemSearch(self):
		books = ecs.ItemSearch("python", SearchIndex="Books")
		self.assert_(len(books) > 200, "We are expect more than 200 books are returned.")
		self.assertNotEqual(books[100], None)
	
	def testSimilarityLookup(self):
		books = ecs.SimilarityLookup("0596009259")
		for book in books:
			self.dump(book)
		self.assert_(len(books) > 9, "We are expect more than 9 books are returned.")

class CarteTest( unittest.TestCase ):
	def setUp(self):
		# prepare the python books to add 
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.books = ecs.ItemSearch("python", SearchIndex="Books")
		self.carte = None

	def testCarteCreate(self):
		items = (self.books[0], self.books[1], self.books[2])
		for i in range(3):
			setattr(items[i], "Quantity", i+1)

		self.cart = ecs.CartCreate(items)
		for i in range(3):
			self.assertEqual(self.books[i].ASIN, self.cart[i].ASIN)
			self.assertEqual(self.books[i].Quantity, int(self.cart[i].Quantity))
		


if __name__ == "__main__" :
	unittest.main()

