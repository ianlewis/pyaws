"""Python wrapper for AWS E-Commerce Serive APIs.

Based upon pyamazon (http://www.josephson.org/projects/pyamazon/) with 
efforts to meet the latest AWS specification.

The Amazon's web APIs specication is described here:
  http://www.amazon.com/webservices

You need a Amazon-provided license key to use these services.
Follow the link above to get one.  These functions will look in
several places (in this order) for the license key:
- the "license_key" argument of each function
- the module-level LICENSE_KEY variable (call setLicense once to set it)
- an environment variable called AMAZON_LICENSE_KEY
- foo would return the python object, XMLfoo returns the DOM object


TODO: 
  - Add more decriptions about this module. 
"""

import os, urllib, string, inspect
from xml.dom import minidom

__author__ = "Kun Xi < kunxi@kunxi.org >"
__version__ = "0.0.1"
__license__ = "GPL"


# Package-wide variables:
LICENSE_KEY = None;
HTTP_PROXY = None
LOCALE = "us"
VERSION = "2005-10-05"


_supportedLocales = {
		"us" : (None, "webservices.amazon.com"),   
		"uk" : ("uk", "webservices.amazon.co.uk"),
		"de" : ("de", "webservices.amazon.de"),
		"jp" : ("jp", "webservices.amazon.co.jp"),
		"fr" : ("fr", "webservices.amazon.fr"),
		"ca" : ("ca", "webservices.amazon.ca")
	}

_licenseKeys = (
	(lambda key: key),
	(lambda key: LICENSE_KEY), 
	(lambda key: os.environ.get('AWS_LICENSE_KEY', None))
   )

# Exception class
class AWSException(Exception) : pass
class NoLicenseKey(AWSException) : pass
class BadLocale(AWSException) : pass
# Runtime exception
class ExactParameterRequirement(AWSException): pass
class ExceededMaximumParameterValues(AWSException): pass
class InsufficientParameterValues(AWSException): pass
class InternalError(AWSException): pass
class InvalidEnumeratedParameter(AWSException): pass
class InvalidISO8601Time(AWSException): pass
class InvalidOperationForMarketplace(AWSException): pass
class InvalidOperationParameter(AWSException): pass
class InvalidParameterCombination(AWSException): pass
class InvalidParameterValue(AWSException): pass
class InvalidResponseGroup(AWSException): pass
class InvalidServiceParameter(AWSException): pass
class InvalidSubscriptionId(AWSException): pass
class InvalidXSLTAddress(AWSException): pass
class MaximumParameterRequirement(AWSException): pass
class MinimumParameterRequirement(AWSException): pass
class MissingOperationParameter(AWSException): pass
class MissingParameterCombination(AWSException): pass
class MissingParameters(AWSException): pass
class MissingParameterValueCombination(AWSException): pass
class MissingServiceParameter(AWSException): pass
class ParameterOutOfRange(AWSException): pass
class ParameterRepeatedInRequest(AWSException): pass
class RestrictedParameterValueCombination(AWSException): pass
class XSLTTransformationError(AWSException): pass


class Bag : pass

# Utilities functions

def _checkLocaleSupported(locale):
	if not _supportedLocales.has_key(locale):
		raise BadLocale, ("Unsupported locale. Locale must be one of: %s" %
			string.join(_supportedLocales, ", "))


def setLocale(locale):
	"""set locale"""
	global LOCALE
	_checkLocaleSupported(locale)
	LOCALE = locale


def getLocale():
	"""get locale"""
	return LOCALE


def setLicenseKey(license_key=None):
	"""set license key

	license key can come from any number of locations;
	see module docs for search order"""

	global LICENSE_KEY
	for get in _licenseKeys:
		rc = get(license_key)
		if rc: 
			LICENSE_KEY = rc;
			return;
	raise NoLicenseKey, ("Please get the license key from  http://www.amazon.com/webservices")


def getLicenseKey():
	"""get license key"""
	if not LICENSE_KEY:
		raise NoLicenseKey, ("Please get the license key from  http://www.amazon.com/webservices")
		
	return LICENSE_KEY
	

def getVersion():
	"""get version"""
	return VERSION


def setVersion(version):
	global VERSION
	VERSION = version
	

def buildRequest(argv):
	"""Build the REST Url from argv"""
	url = "http://" + _supportedLocales[LOCALE][1] + "/onca/xml?Service=AWSECommerceService"
	for k,v in argv.items():
		if v:
			url += '&%s=%s' % (k,v)

	print "url=", url
	return url;


def buildException(els):
	"""Build the exception according to the returned error
	Notice: We just return the first error"""

	error = els[0]
	class_name = error.childNodes[0].firstChild.data[4:]
	msg = error.childNodes[1].firstChild.data 

	e = globals()[ class_name ](msg)
	return e


def query(url):
	"""Send the query url and return the DOM"""
	u = urllib.FancyURLopener(HTTP_PROXY)
	usock = u.open(url)
	dom = minidom.parse(usock)
	usock.close()

	errors = dom.getElementsByTagName('Error')
	if errors:
		e = buildException(errors)
		raise e
	
	return dom


def rawIterator(XMLSearch, arguments, plugins, kwItems, kwItem):
	dom = XMLSearch(** arguments)
	plugins['isCollective'] = lambda x: x == kwItems
	plugins['isCollected'] = lambda x: x == kwItem
	items = unmarshal(dom.getElementsByTagName(kwItems).item(0), plugins, wrappedIterator([]))
	return items

class wrappedIterator(list):
	'''A built-in list wrapper, we can add attributes later'''
	pass
	

class pagedIterator:
	'''Return a page-based iterator'''

	def __init__(self, XMLSearch, arguments, plugins, kwPage, kwItems, kwItem):
		"""XMLSearch: the callback function that returns the DOM
		arguments: the arguments for XMLSearch
		kwPage, kwItems, kwItem: page, items, item keyword to organize the object
		"""
		# TODO: kwItem is useless
		self.search = XMLSearch 
		self.arguments = arguments 
		self.keywords ={ 'Page':kwPage, 'Items':kwItems, 'Item':kwItem } 
		plugins['isCollective'] = lambda x: x == kwItems
		plugins['isCollected'] = lambda x: x == kwItem
		self.plugins = plugins
		self.page = arguments[kwPage] or 1
		self.index = 0
		dom = self.search(** self.arguments)
		self.items = unmarshal(dom.getElementsByTagName(kwItems).item(0), plugins, wrappedIterator())
		try:
			self.len = int(dom.getElementsByTagName("TotalResults").item(0).firstChild.data)
		except AttributeError, e:
			self.len = len(self.items)

	def __len__(self):
		return self.len

	def __iter__(self):
		return self

	def next(self):
		if self.index < self.len:
			self.index = self.index + 1
			return self.__getitem__(self.index-1)
		else:
			raise StopIteration

	def __getitem__(self, key):
		try:
			num = int(key)
		except TypeError, e:
			raise e

		if num >= self.len:
			raise IndexError

		page = num / 10 + 1
		index = num % 10
		if page != self.page:
			self.arguments[self.keywords['Page']] = page
			dom = self.search(** self.arguments)
			self.items = unmarshal(dom.getElementsByTagName(self.keywords['Items']).item(0), self.plugins, wrappedIterator())
			self.page = page

		return self.items[index]


def createList(dom, kwItems, plugins):
	items = unmarshal(dom.getElementsByTagName(kwItems).item(0), plugins, wrappedIterator([]))
	try:
		total = int(dom.getElementsByTagName("TotalResults").item(0).firstChild.data)
	except AttributeError, e:
		total = len(items)
	return (items, total)

def unmarshal(element, plugins=None, rc=None):
	"""this core function populate the object using the DOM, 
	which is inspired by Mark Pilgrim (f8dy@diveintomark.org)"""

	if(rc == None):
		rc = Bag()

	if(plugins == None):
		plugins = {}

	childElements = [e for e in element.childNodes if isinstance(e, minidom.Element)]

	if childElements:
		for child in childElements:
			key = child.tagName
			if hasattr(rc, key):
				if type(getattr(rc, key)) <> type([]):
					setattr(rc, key, [getattr(rc, key)])
				setattr(rc, key, getattr(rc, key) + [unmarshal(child, plugins)])
			elif isinstance(child, minidom.Element):
				if plugins.has_key('isPrivoted') and plugins['isPrivoted'](child.tagName):
						unmarshal(child, plugins, rc)
				elif plugins.has_key('isBypassed') and plugins['isBypassed'](child.tagName):
					continue
				elif plugins.has_key('isCollective') and plugins['isCollective'](child.tagName):
					setattr(rc, key, unmarshal(child, plugins, wrappedIterator([])))
				elif plugins.has_key('isCollected') and plugins['isCollected'](child.tagName):
					rc.append(unmarshal(child, plugins))
				else:
					setattr(rc, key, unmarshal(child, plugins))
	else:
		rc = "".join([e.data for e in element.childNodes if isinstance(e, minidom.Text)])
	return rc


	
# User interfaces

def ItemLookup(ItemId, IdType=None, SearchIndex=None, MerchantId=None, Condition=None, DeliveryMethod=None, ISPUPostalCode=None, OfferPage=None, ReviewPage=None, VariationPage=None, ResponseGroup=None, AWSAccessKeyId=None): 
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	plugins = {'isPrivoted': lambda x: x == 'ItemAttributes'}
	return pagedIterator(XMLItemLookup, argv, plugins, 'OfferPage', 'Items', 'Item')
	
def XMLItemLookup(ItemId, IdType=None, SearchIndex=None, MerchantId=None, Condition=None, DeliveryMethod=None, ISPUPostalCode=None, OfferPage=None, ReviewPage=None, VariationPage=None, ResponseGroup=None, AWSAccessKeyId=None): 
	Operation = "ItemLookup"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	return query(buildRequest(argv))

def ItemSearch(Keywords, SearchIndex="Blended", Availability=None, Title=None, Power=None, BrowseNode=None, Artist=None, Author=None, Actor=None, Director=None, AudienceRating=None, Manufacturer=None, MusicLabel=None, Composer=None, Publisher=None, Brand=None, Conductor=None, Orchestra=None, TextStream=None, ItemPage=None, Sort=None, City=None, Cuisine=None, Neighborhood=None, MinimumPrice=None, MaximumPrice=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	plugins = {'isPrivoted': lambda x: x == 'ItemAttributes'}
	return pagedIterator(XMLItemSearch, argv, plugins, "ItemPage", 'Items', 'Item')

def XMLItemSearch(Keywords, SearchIndex="Blended", Availability=None, Title=None, Power=None, BrowseNode=None, Artist=None, Author=None, Actor=None, Director=None, AudienceRating=None, Manufacturer=None, MusicLabel=None, Composer=None, Publisher=None, Brand=None, Conductor=None, Orchestra=None, TextStream=None, ItemPage=None, Sort=None, City=None, Cuisine=None, Neighborhood=None, MinimumPrice=None, MaximumPrice=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	Operation = "ItemSearch"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	Keywords = urllib.quote(Keywords)
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	return query(buildRequest(argv))

def SimilarityLookup(ItemId, SimilarityType=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	plugins = {'isPrivoted': lambda x: x == 'ItemAttributes'}
	return rawIterator(XMLSimilarityLookup, argv, plugins, 'Items' , 'Item')

def XMLSimilarityLookup(ItemId, SimilarityType=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	Operation = "SimilarityLookup"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	return query(buildRequest(argv))

# ListOperation
def ListLookup(ListType, ListId, ProductPage=None, ProductGroup=None, Sort=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	plugins = {'isPrivoted': lambda x: x == 'ItemAttributes'}
	return pagedIterator(XMLListLookup, argv, plugins, 'ProductPage', 'Lists' , 'List')

def XMLListLookup(ListType, ListId, ProductPage=None, ProductGroup=None, Sort=None, MerchantId=None, Condition=None, DeliveryMethod=None, ResponseGroup=None, AWSAccessKeyId=None):  
	Operation = "ListLookup"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	return query(buildRequest(argv))

def ListSearch(ListType, Name=None, FirstName=None, LastName=None, Email=None, City=None, State=None, ListPage=None, ResponseGroup=None, AWSAccessKeyId=None):
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	plugins = {'isPrivoted': lambda x: x == 'ItemAttributes'}
	return pagedIterator(XMLListSearch, argv, plugins, 'ListPage', 'Lists', 'List')

def XMLListSearch(ListType, Name=None, FirstName=None, LastName=None, Email=None, City=None, State=None, ListPage=None, ResponseGroup=None, AWSAccessKeyId=None):
	Operation = "ListSearch"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	return query(buildRequest(argv))

#Remote Shopping Cart Operations
def CartCreate(Items, Quantities, ResponseGroup=None, AWSAccessKeyId=None):
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	dom =  XMLCartCreate(** argv)
	return _cartOperation(dom)

def XMLCartCreate(Items, Quantities, ResponseGroup=None, AWSAccessKeyId=None):
	Operation = "CartCreate"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	for x in ('Items', 'Quantities'):
		del argv[x]

	_fromListToItems(argv, Items, 'ASIN', Quantities)
	return query(buildRequest(argv))

def CartAdd(Cart, Items, Quantities, ResponseGroup=None, AWSAccessKeyId=None):
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	dom =  XMLCartAdd(** argv)
	return _cartOperation(dom)

def XMLCartAdd(Cart, Items, Quantities, ResponseGroup=None, AWSAccessKeyId=None):
	Operation = "CartAdd"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	CartId = Cart.CartId
	HMAC = urllib.quote(Cart.HMAC)
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	for x in ('Items', 'Cart', 'Quantities'):
		del argv[x]

	_fromListToItems(argv, Items, 'ASIN', Quantities)
	return query(buildRequest(argv))

def CartGet(Cart, ResponseGroup=None, AWSAccessKeyId=None):
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	dom =  XMLCartGet(** argv)
	return _cartOperation(dom)

def XMLCartGet(Cart, ResponseGroup=None, AWSAccessKeyId=None):
	Operation = "CartGet"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	CartId = Cart.CartId
	HMAC = urllib.quote(Cart.HMAC)
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	del argv['Cart']

	return query(buildRequest(argv))

def CartModify(Cart, Items, Actions, ResponseGroup=None, AWSAccessKeyId=None):
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	dom =  XMLCartModify(** argv)
	return _cartOperation(dom)

def XMLCartModify(Cart, Items, Actions, ResponseGroup=None, AWSAccessKeyId=None):
	Operation = "CartModify"
	AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
	CartId = Cart.CartId
	HMAC = urllib.quote(Cart.HMAC)
	argv = inspect.getargvalues(inspect.currentframe())[-1]
	for x in ('Cart', 'Items', 'Actions'):
		del argv[x]

	_fromListToItems(argv, Items, 'CartItemId', Actions)
	return query(buildRequest(argv))
	

def _fromListToItems(argv, items, id, actions):
	for i in range(len(items)):
		argv["Item.%d.%s" % (i+1, id)] = getattr(items[i], id);
		action = actions[i]
		if isinstance(action, int):
			argv["Item.%d.Quantity" % (i+1)] = action
		else:
			argv["Item.%d.Action" % (i+1)] = action


def _cartOperation(dom):
	plugins = {'isBypassed': lambda x: x == 'Request',
		'isCollective': lambda x: x in ('CartItems', 'SavedForLaterItems'),
		'isCollected': lambda x: x in ('CartItem', 'SavedForLaterItem') }
	return unmarshal(dom.getElementsByTagName('Cart').item(0), plugins)


if __name__ == "__main__" :
	setLicenseKey("1MGVS72Y8JF7EC7JDZG2")
	books = ItemSearch("python", SearchIndex="Books")
	items = (books[0], books[1], books[2])
	qs = (1, 3, 5)
	cart = CartCreate(items, qs)
	import pdb
	pdb.set_trace()

