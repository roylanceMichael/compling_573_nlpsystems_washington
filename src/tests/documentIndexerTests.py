import unittest
import extract.documentIndexer
import extract.document

rootFolder = "../doc/"

class DocumentIndexerTests(unittest.TestCase):
	def test_simpleTopicGet(self):
		# arrange
		fileName = "../doc/nyt/1998/19980601_NYT"

		# act
		foundDocumentIndexer = None
		for documentIndexer in extract.documentIndexer.DocumentIndexer.factoryMultiple(fileName):
			foundDocumentIndexer = documentIndexer
			break

		# assert
		foundDocument =extract.document.Document.factoryFromIndexer(foundDocumentIndexer)

		self.assertTrue(foundDocument != None)