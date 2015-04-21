import glob
import document

filePathTemplate = "%s%s/%s/%s%s_%s"
trainingFilePathTemplate = "%s/%s/%s_%s%s.xml"


# file paths are:
# /corpora/LDC/LDC08T25/data
class DocumentRepository:
	def __init__(self, rootDocumentFolder, trainRootFolder, topics):
		self.rootDocumentFolder = rootDocumentFolder
		self.trainRootFolder = trainRootFolder
		self.topics = {}
		self.fileIdDictionary = {}

		for topic in topics:
			self.topics[topic.id] = topic

	def getDocumentsGroupedByTopic(self, useDocsetA=True):
		for key in self.topics:
			yield self.topics[key]

			for foundDocument in self.getDocumentsByTopic(key):
				yield foundDocument

	def getDocumentsByTopic(self, topicId, useDocsetA=True):
		if topicId is None or topicId not in self.topics:
			return

		foundTopic = self.topics[topicId]
		docsetList = foundTopic.docsetA

		if not useDocsetA:
			docsetList = foundTopic.docsetB

		for docId in docsetList:
			foundDocument = self.getDocument(docId)

			if foundDocument is not None:
				yield foundDocument

	def isTest(self, key):
		return "ENG" not in key

	def buildTestFileName(self, docId):
		# first, find folder
		folderName = docId[0:3].lower()
		year = docId[3:7]
		fileId = docId[7:11]
		docNumber = docId[12:16]

		#### HACK!  special name weirdness for XIN documents.  they have a weird folder name  ####
		fileNameHack = folderName.upper()
		if folderName == 'xie':
			fileNameHack = 'XIN'

		# does our file exist?
		fileName = filePathTemplate % (self.rootDocumentFolder, folderName, year, year, fileId, fileNameHack)
		globFileNameArray = glob.glob(fileName + "*")

		if len(globFileNameArray) > 0:
			return globFileNameArray[0]
		return fileName

	def buildTrainFileName(self, docId):
		# first, find folder
		# APW_ENG_20050902.0312
		folderName = docId[0:7].lower()
		year = docId[8:11]
		fileId = docId[11:14]

		# does our file exist?
		fileName = trainingFilePathTemplate % (self.trainRootFolder, folderName, folderName, year, fileId)
		return fileName

	def getDocument(self, docId):
		# example id:
		# APW19990421.0284
		if docId is None or len(docId) < 16:
			return None

		cleansedDocId = docId.strip()

		if cleansedDocId in self.fileIdDictionary:
			return self.fileIdDictionary[cleansedDocId]

		# first, find folder
		fileName = ""
		if self.isTest(docId):
			fileName = self.buildTestFileName(docId)
		else:
			fileName = self.buildTrainFileName(docId)

		foundDocument = document.Document.factoryForSpecificDocNo(fileName, cleansedDocId)
		if foundDocument != None:
			self.fileIdDictionary[foundDocument.docNo.strip()] = foundDocument

		return foundDocument