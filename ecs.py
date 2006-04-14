"""Python wrapper for AWS E-Commerce Serive APIs.

Based upon pyamazon ( http://www.josephson.org/projects/pyamazon/ ) with 
efforts to meet the latest AWS specification.

The Amazon's web APIs specication is described here:
  http://www.amazon.com/webservices

You need a Amazon-provided license key to use these services.
Follow the link above to get one.  These functions will look in
several places (in this order) for the license key:
- the "license_key" argument of each function
- the module-level LICENSE_KEY variable (call setLicense once to set it)
- an environment variable called AMAZON_LICENSE_KEY


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
        "ca" : ("ca", "webservices.amazon.ca" )
    }

_licenseKeys = (
    (lambda key: key ),
    (lambda key: LICENSE_KEY ), 
    (lambda key: os.environ.get('AWS_LICENSE_KEY', None))
    )

# Exception class
class AWSException( Exception ) : pass
class NoLicenseKey( AWSException ) : pass
class BadLocale( AWSException ) : pass
class InvalidParameterValue( AWSException ): pass

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
    raise NoLicenseKey, ("Please get the license key from  http://www.amazon.com/webservices" )


def getLicenseKey(license_key = None):
    """get license key"""
    return LICENSE_KEY
    

def getVersion():
    """get version"""
    return VERSION


def setVersion(version):
    global VERSION
    VERSION = version
    

def buildRequest( argv ):
    url = "http://" + _supportedLocales[LOCALE][1] + "/onca/xml?Service=AWSECommerceService"
    for k,v in argv:
        if v:
            url += '&%s=%s' % (k,v)
    return url;


def buildException( els ):
    # We just care the first error.
    error = els[0]
    class_name = error.childNodes[0].firstChild.data[4:]
    msg = error.childNodes[1].firstChild.data 

    e = globals()[ class_name ](msg)
    return e



    
# User interfaces

def ItemLookup( ItemId, IdType=None, AWSAccessKeyId=None ): 
    Operation = "ItemLookup"
    AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
    argv = inspect.getargvalues( inspect.currentframe() )[-1].items();
    url = buildRequest( argv );
    return url;


def ItemSearch( Keywords, SearchIndex="Blended", AWSAccessKeyId=None ):  
    Operation = "ItemSearch"
    AWSAccessKeyId = AWSAccessKeyId or LICENSE_KEY
    Keywords = urllib.quote(Keywords)
    argv = inspect.getargvalues( inspect.currentframe() )[-1].items();
    url = buildRequest( argv );
    return url;
    
# core functions

def query( url ):
    u = urllib.FancyURLopener( HTTP_PROXY )
    usock = u.open(url)
    dom = minidom.parse(usock)
    usock.close()

    errors = dom.getElementsByTagName('Error')
    if errors:
        e = buildException( errors )
        raise e
    
    return dom


def unmarshal(element):
    rc = Bag()
    childElements = [e for e in element.childNodes if isinstance(e, minidom.Element)]

    if childElements:
        for child in childElements:
            key = child.tagName
            if hasattr(rc, key):
                if type(getattr(rc, key)) <> type([]):
                    setattr(rc, key, [getattr(rc, key)])
                setattr(rc, key, getattr(rc, key) + [unmarshal(child)])
            elif isinstance(child, minidom.Element) :
                # make the first Details element a key
                setattr(rc,key,[unmarshal(child)])
                #dbg: because otherwise 'hasattr' only tests
                #dbg: on the second occurence: if there's a
                #dbg: single return to a query, it's not a
                #dbg: list. This module should always
                #dbg: return a list of Details objects.
            else:
                setattr(rc, key, unmarshal(child))
    else:
        rc = "".join([e.data for e in element.childNodes if isinstance(e, minidom.Text)])
    return rc

if __name__ == "__main__" :
    setLicenseKey("1MGVS72Y8JF7EC7JDZG2")
    dom = query( ItemLookup( "0596002815" ) )
    print dom.toprettyxml()
    items = dom.getElementsByTagName('Items').item(0)
    books = unmarshal(items)
    print dir( books )
    print dir( books.Item )
