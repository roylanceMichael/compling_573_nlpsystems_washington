import os.listdir
import os.path


class DocumentIdRepository:
	def __init__(rootDocumentFolder, topicXml):
		self.rootDocumentFolder = rootDocumentFolder
		self.topicXml = topicXml
		self.fileIdDictionary = { }

	def generateFileIdDictionary(self, rootFolder):
		for folder in os.listdir(rootFolder):
			if os.path.isfile(folder):
				print folder
			else:
				generateFileIdDictionary(folder)

