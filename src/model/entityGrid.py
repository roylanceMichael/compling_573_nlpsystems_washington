__author__ = 'thomas'

from textrazor.textrazor import TextRazor
import numpy

subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0

class EntityGrid:
	# build entity grid
	def __init__(self, docModel):
		self.docModel = docModel
		self.sentences = self.docModel.cleanSentences()
		self.fullText = " \n".join(self.sentences)
		self.textRazor = TextRazor(api_key="99cb513961595f163f4ab253a8aaf167970f8a49981e229a3c8505a0", \
				   extractors=["entities", "topics", "words", "dependency-trees"])

		nerResults = self.getEntities(self.fullText)
		self.allEntities = nerResults[0]
		self.allWords = nerResults[1]
		self.matrixIndices = self.getMatrixIndices()
		self.numUniqueEntities = len(self.matrixIndices)
		self.grid = self.fillMatrix()


	def makeEmptyMatrix(self):
		numpyMatrix = list()
		for index in self.matrixIndices.values():
			numpyMatrix.append(numpy.array(self.numUniqueEntities))
		return numpyMatrix

	def getCoreferents(self, word):
		# this will eventually check the coref list
		return word

	def fillMatrix(self):
		matrix = self.makeEmptyMatrix()
		sNum = 0
		for sentence in self.sentences:
			snerResult = self.getEntities(sentence)
			entities = snerResult[0]
			words = snerResult[1]
			for entity in entities:
				matrix[sNum][entity.entityId] = 1.0
			sNum += 1
		return matrix

	def getEntities(self, text):
		#get entities
		response = self.textRazor.analyze(text)
		return [response.entities(), response.words()]

	def getMatrixIndices(self):
		matrixIndices = {}
		i = 0
		for entity in self.allEntities:
			if not entity.entityId in matrixIndices.keys():
				matrixIndices[entity.entityId] = i
				i += 1
		return matrixIndices