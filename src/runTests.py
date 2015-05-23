# Author:  Mike Roylance (roylance@uw.edu)
#
# run tests
#

# http://stackoverflow.com/questions/1732438/how-to-run-all-python-unit-tests-in-a-directory - thank you!
import unittest

testModules = [  'tests.kmeansTests'
				#'tests.documentTests',
				 #'tests.topicReaderTests',
				 #'tests.documentRepositoryTests',
				 # 'tests.documentIndexerTests',
				 # 'tests.npClusteringTests',
				 # 'tests.coreferenceTests',
				 # 'tests.coherenceTests'
				 ]

suite = unittest.TestSuite()

for testModule in testModules:
	suite.addTest(unittest.defaultTestLoader.loadTestsFromName(testModule))

unittest.TextTestRunner().run(suite)