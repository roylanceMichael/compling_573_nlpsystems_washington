import os.path
import document

filePathTemplate = "%s/%s/%s/%s%s_%s"

class DocumentRepository:
	def __init__(self, rootDocumentFolder, topics):
		self.rootDocumentFolder = rootDocumentFolder
		self.topics = { }
		self.fileIdDictionary = { }

		for topic in topics:
			self.topics[topic.id] = topic

	def getDocumentsGroupedByTopic(self, useDocsetA=True):
		for key in self.topics:
			yield self.topics[key]

			for foundDocument in self.getDocumentsByTopic(key):
				yield foundDocument

	def getDocumentsByTopic(self, topicId, useDocsetA=True):
		if topicId == None or topicId not in self.topics:
			return

		foundTopic = self.topics[topicId]

		docsetList = foundTopic.docsetA

		if not useDocsetA:
			docsetList = foundTopic.docsetB

		for docId in docsetList:
			foundDocument = self.getDocument(docId)

			if foundDocument != None:
				yield foundDocument

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
		fileName = filePathTemplate % (self.rootDocumentFolder, folderName, year, year, fileId, folderName.upper())

		for foundDocument in document.Document.factoryMultiple(fileName, True, False):
			self.fileIdDictionary[foundDocument.docNo.strip()] = foundDocument

		if cleansedDocId in self.fileIdDictionary:
			return self.fileIdDictionary[cleansedDocId]
		return None