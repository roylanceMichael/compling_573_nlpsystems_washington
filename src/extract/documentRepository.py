import os.path
import document

filePathTemplate = "%s/%s/%s%s_%s"

class DocumentRepository:
	def __init__(rootDocumentFolder, topics):
		self.rootDocumentFolder = rootDocumentFolder
		self.topics = topics
		self.fileIdDictionary = { }

	def getDocument(self, docId):
		# example id:
		# APW19990421.0284

		if docId == None or len(docId) < 16:
			return None

		cleansedDocId = docId.strip()

		if cleansedDocId in self.fileIdDictionary:
			return self.fileIdDictionary[cleansedDocId]

		# first, find folder
		folderName = docId[0:3].lower()
		year = docId[3:7]
		fileId = docId[7:11]
		docNumber = docId[12:16]

		# does our file exist?
		fileName = filePathTemplate % (folderName, year, year, fileId, folderName.upper())

		for foundDocument in document.factoryMultiple(fileName, True, False):
			self.fileIdDictionary[foundDocument.docNo.strip()] = foundDocument

		if cleansedDocId in self.fileIdDictionary:
			return self.fileIdDictionary[cleansedDocId]
		return None