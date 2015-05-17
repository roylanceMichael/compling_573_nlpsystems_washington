__author__ = 'mroylance'

import numpy
import random

subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0


#
# AsasEntityGrid:  generates an entity grid ala Barsilay and Lapata (2005)
#			   uses ASAS to mark named entities.
#
class AsasEntityGrid:
	# build entity grid
	def __init__(self, sentences):
		self.sentences = sentences
		self.entities = []

		for sentence in sentences:
			for entity in sentence.entities:
				self.entities.append(entity)

		self.matrixIndices = self.getMatrixIndices()
		self.numUniqueEntities = len(self.matrixIndices)
		self.grid = self.fillMatrix()

	def makeEmptyMatrix(self):
		numpyMatrix = list()
		for sentence in self.sentences:
			numpyMatrix.append(numpy.zeros(self.numUniqueEntities))
		return numpyMatrix

	def setEntityUseType(self, entityId, matrix, sNum, score):
		matrix[sNum][self.matrixIndices[entityId]] = max(score, matrix[sNum][self.matrixIndices[entityId]])

	def fillMatrix(self):
		matrix = self.makeEmptyMatrix()

		for sentence in self.sentences:
			for entity in sentence.entityScores:
				self.setEntityUseType(entity[4], matrix, sentence.sentenceNum, sentence.entityScores[entity])

		return matrix

	def getMatrixIndices(self):
		matrixIndices = {}
		i = 0
		for entity in self.entities:
			if entity[4] not in matrixIndices.keys():
				matrixIndices[entity[4]] = i
				i += 1
		return matrixIndices

	@staticmethod
	def scoreFromToken(scoreToken):
		score = 0.0
		if scoreToken == "s":
			score = 3.0
		elif scoreToken == "o":
			score = 2.0
		elif scoreToken == "x":
			score = 1.0
		return score

	@staticmethod
	def tokenFromScore(score):
		scoreToken = "-"
		if score == 1.0:
			scoreToken = "x"
		elif score == 2.0:
			scoreToken = "o"
		elif score == 3.0:
			scoreToken = "s"
		return scoreToken

	@staticmethod
	def getLongestEntity(entities):
		longestLen = 0
		longestEntity = None
		for entity in entities:
			if len(entity.matched_words) > longestLen:
				longestLen = len
				longestEntity = entity.id
		return longestEntity

	def printMatrix(self):
		for index in self.matrixIndices:
			print index + " - ",
		print "\n"
		score = 0.0
		for sNum in range(0, len(self.grid)):
			row = ""
			for index in self.matrixIndices:
				try:
					score = self.grid[sNum][self.matrixIndices[index]]
				except IndexError:
					print "error"


				row += self.tokenFromScore(score) + " "

			print row


testText = [
	"The Justice Department is conducting an anti-trust \
trial against Microsoft Corp. with evidence that \
the company is increasingly attempting to crush \
competitors.",
	"Microsoft is accused of trying to forcefully buy into \
markets where its own products are not competitive \
enough to unseat established brands.",
	"The case revolves around evidence of Microsoft \
aggressively pressuring Netscape into merging \
browser software.",
	"Microsoft claims its tactics are commonplace and \
good economically.",
	"The government may file a civil suit ruling \
that conspiracy to curb competition through \
collusion is a violation of the Sherman Act.",
	"Microsoft continues to show increased earnings despite \
the trial."]


# grid = EntityGrid(DummyDocModel(testText))
# grid.printMatrix()
# featureVector = FeatureVector(grid)
# featureVector.printVector()