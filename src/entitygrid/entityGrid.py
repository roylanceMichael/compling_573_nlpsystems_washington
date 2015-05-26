__author__ = 'thomas'

import random

subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0


#
# FeatureVector:  class for generating and holding the feature vector as svmlight expects it
#
class FeatureVector:
	def __init__(self, entityGrid, docIndex):
		self.types = ['-', 'x', 'o', 's']
		self.transitionMap = {}
		self.docIndex = docIndex
		self.entityGrid = entityGrid
		self.transitions = self.generateTransitions()

	def getTransitionIndexFromTransitionString(self, transitionString):
		return self.transitionMap[transitionString]

	def getTransitionStringFromTransitionIndex(self, transitionIndex):
		for fromType in self.types:
			for toType in self.types:
				transitionString = fromType + toType
				testIndex = self.transitionMap[transitionString]
				if testIndex == transitionIndex:
					return transitionString
		raise IndexError("bad transition index")

	def generateTransitions(self):

		numTransitions = float((len(self.entityGrid.sentences) - 1) * len(self.entityGrid.matrixIndices))
		# make transitions dictionary
		transitions = {}
		for fromType in self.types:
			for toType in self.types:
				try:
					transitions[fromType][toType] = 0
				except KeyError:
					transitions[fromType] = {}
					transitions[fromType][toType] = 0

		# make the transition map
		transitionIndex = 1
		for fromType in self.types:
			for toType in self.types:
				transitionString = fromType + toType
				self.transitionMap[transitionString] = transitionIndex
				transitionIndex += 1

		# fill in transitions with actual transitions map
		for sIdx in range(0, len(self.entityGrid.sentences) - 1):
			s1 = self.entityGrid.grid[sIdx]
			s2 = self.entityGrid.grid[sIdx + 1]
			for entityId in self.entityGrid.matrixIndices:
				start = self.entityGrid.tokenFromScore(s1[self.entityGrid.matrixIndices[entityId]])
				end = self.entityGrid.tokenFromScore(s2[self.entityGrid.matrixIndices[entityId]])
				transitions[start][end] += 1

		for fromType in self.types:
			for toType in self.types:
				try:
					transitions[fromType][toType] /= numTransitions
				except ZeroDivisionError:
					print "ERROR: No Transitions.  This should have been dealt with.  wtf?"
		return transitions

	def printVector(self):
		for fromType in self.types:
			for toType in self.types:
				print fromType + toType + ":" + str(round(self.transitions[fromType][toType], 2)) + " ",
		print "\n"

	def printVectorWithIndices(self):
		outString = ""
		for fromType in self.types:
			for toType in self.types:
				featureIndex = str(self.getTransitionIndexFromTransitionString(fromType + toType))
				featureValue = str(round(self.transitions[fromType][toType], 2))
				outString += featureIndex + ":" + featureValue + " "
		outString += "\n"
		print outString

	def getVector(self, rank):
		vector = []
		for fromType in self.types:
			for toType in self.types:
				featureIndex = self.getTransitionIndexFromTransitionString(fromType + toType)
				featureValue = self.transitions[fromType][toType]
				if featureValue > 0.0:
					vector.append((featureIndex, featureValue))
		finalVector = (rank, vector, self.docIndex)
		return finalVector

#
# EntityGrid:  generates an entity grid ala Barsilay and Lapata (2005)
#			   uses TextRazor to mark named entities.
#
class EntityGrid:
	# build entity grid
	def __init__(self, sentences):
		self.sentences = sentences
		self.numSentences = len(sentences)
		self.grid = None
		self.matrixIndices = None

	def setEntityUseType(self, entityId, matrix, sNum, score):
		matrix[sNum][self.matrixIndices[entityId]] = max(score, matrix[sNum][self.matrixIndices[entityId]])

	# remove all unused entities and build a new grid
	def compressMatrix(self):
		newMatrixIndices = {}
		usedEntityIds = self.getUsedEntityIds()
		newMatrix = self.makeEmptyMatrix(len(usedEntityIds))
		for sNum in range(0, len(self.grid)):
			idx = 0
			for entityId in usedEntityIds:
				newMatrix[sNum][idx] = self.grid[sNum][self.matrixIndices[entityId]]
				newMatrixIndices[entityId] = idx
				idx += 1
		self.grid = newMatrix
		self.matrixIndices = newMatrixIndices

	def makeEmptyMatrix(self, width):
		matrix = list()
		for i in range(0, self.numSentences):
			matrix.append([0.0] * width)
		return matrix

	def getMatrixIndices(self, entityIds):
		matrixIndices = {}
		i = 0
		for entity in entityIds:
			if entityIds not in matrixIndices.keys():
				matrixIndices[entity] = i
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

	# get the entity ids that are being used.
	def getUsedEntityIds(self):
		usedEntities = []
		for index in self.matrixIndices:
			unused = True
			for sNum in range(0, len(self.grid)):
				score = self.grid[sNum][self.matrixIndices[index]]
				if score != 0.0:
					unused = False
					break
			if not unused:
				usedEntities.append(index)
		return usedEntities


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




#
# DummyDocModel: super duper simple doc model that only has sentences.
#
class DummyDocModel:
	def __init__(self, sentences):
		self.sentences = sentences

	def cleanSentences(self):
		return self.sentences

	def randomizeSentences(self):
		random.shuffle(self.sentences)

