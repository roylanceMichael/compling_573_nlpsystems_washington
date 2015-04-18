# mike roylance
# http://stackoverflow.com/questions/1732438/how-to-run-all-python-unit-tests-in-a-directory - thank you!
import unittest

testModules = [
    'tests.documentTests',
    'tests.topicReaderTests',
    'tests.documentRepositoryTests',
    'tests.documentIndexerTests',
    ]

suite = unittest.TestSuite()

for testModule in testModules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(testModule))

unittest.TextTestRunner().run(suite)