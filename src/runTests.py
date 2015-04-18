# mike roylance
# http://stackoverflow.com/questions/1732438/how-to-run-all-python-unit-tests-in-a-directory - thank you!
import unittest

testModules = [
    'tests.documentTests',
    'tests.topicReaderTests',
    ]

suite = unittest.TestSuite()

for testModule in testModules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(testModule, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(testModule))

unittest.TextTestRunner().run(suite)