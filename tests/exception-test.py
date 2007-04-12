import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class ExceptionsTest( unittest.TestCase ):

	def testBadLicenseKey(self):
		ecs.setLicenseKey( "1MGVS72Y8JF7EC7JDZG0" )
		self.assertRaises( ecs.InvalidParameterValue, ecs.ItemLookup, "0596002818" )

	def testDefaultLocale(self):
		self.assertEqual( ecs.getLocale(), "us" )

	def testSetLocale(self):
		ecs.setLocale( "fr" )
		self.assertEqual( ecs.getLocale(), "fr" )

	def testBadLocale(self):
		self.assertRaises( ecs.BadLocale, ecs.setLocale, "zh" )

	def testVersion(self):
		self.assertEqual(ecs.getVersion(), "2007-04-04")

	def testOptionPut(self):
		self.assertRaises( ecs.BadOption, ecs.setOptions, {'foo': 3} )


	def testExactParameterRequirement(self):
		pass

	def testExceededMaximumParameterValues(self):
		pass

	def testInsufficientParameterValues(self):
		pass

	def testInternalError(self):
		pass

	def testInvalidEnumeratedParameter(self):
		pass

	def testInvalidISO8601Time(self):
		pass

	def testInvalidOperationForMarketplace(self):
		pass

	def testInvalidOperationParameter(self):
		pass

	def testInvalidParameterCombination(self):
		pass

	def testInvalidParameterValue(self):
		pass

	def testInvalidResponseGroup(self):
		pass

	def testInvalidServiceParameter(self):
		pass

	def testInvalidSubscriptionId(self):
		pass

	def testInvalidXSLTAddress(self):
		pass

	def testMaximumParameterRequirement(self):
		pass

	def testMinimumParameterRequirement(self):
		pass

	def testMissingOperationParameter(self):
		pass

	def testMissingParameterCombination(self):
		pass

	def testMissingParameters(self):
		pass

	def testMissingParameterValueCombination(self):
		pass

	def testMissingServiceParameter(self):
		pass

	def testParameterOutOfRange(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.assertRaises( ecs.ParameterOutOfRange, ecs.ItemSearch, "python", SearchIndex="Books", ItemPage="9999") 


	def testParameterRepeatedInRequest(self):
		pass

	def testRestrictedParameterValueCombination(self):
		pass

	def testXSLTTransformationError(self):
		pass


if __name__ == "__main__" :
	unittest.main()

