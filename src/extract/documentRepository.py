import os.path
import document
import documentIndexer

filePathTemplate = "%s/%s/%s/%s%s_%s"
trainingFilePathTemplate = "%s/%s/%s_%s%s.xml"

# file paths are:
# /corpora/LDC/LDC08T25/data
class DocumentRepository:
	def __init__(self, rootDocumentFolder, trainRootFolder, topics):
		self.rootDocumentFolder = rootDocumentFolder
		self.trainRootFolder = trainRootFolder
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

	def isTest(self, key):
		return "ENG" not in key

	def buildTestFileName(self, docId):
		# first, find folder
		folderName = docId[0:3].lower()
		year = docId[3:7]
		fileId = docId[7:11]
		docNumber = docId[12:16]

		# does our file exist?
		fileName = filePathTemplate % (self.rootDocumentFolder, folderName, year, year, fileId, folderName.upper())
		return fileName

	def buildTrainFileName(self, docId):
		# first, find folder
		# APW_ENG_20050902.0312
		folderName = docId[0:7].lower()
		year = docId[8:11]
		fileId = docId[11:13]

		# does our file exist?
		fileName = trainingFilePathTemplate % (self.trainRootFolder, folderName, folderName.upper(), year, fileId)
		return fileName

	def getDocument(self, docId):
		# example id:
		# APW19990421.0284
		if docId == None or len(docId) < 16:
			return None

		cleansedDocId = docId.strip()

		if cleansedDocId in self.fileIdDictionary:
			return document.Document.factoryFromIndexer(self.fileIdDictionary[cleansedDocId])

		# first, find folder
		fileName = ""
		if self.isTest(docId):
			fileName = self.buildTestFileName(docId)
		else:
			fileName = self.buildTrainFileName(docId)

		for foundDocument in documentIndexer.DocumentIndexer.factoryMultiple(fileName):
			self.fileIdDictionary[foundDocument.docNo.strip()] = foundDocument

		if cleansedDocId in self.fileIdDictionary:
			return document.Document.factoryFromIndexer(self.fileIdDictionary[cleansedDocId])

		return None