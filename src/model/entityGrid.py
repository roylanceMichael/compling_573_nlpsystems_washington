__author__ = 'thomas'

from textrazor.textrazor import TextRazor
import numpy
import random

subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0

# textrazor keys
thomasKey = "99cb513961595f163f4ab253a8aaf167970f8a49981e229a3c8505a0"
mikeKey = "a40db69a54fa0905294e6b604b5dca251e9df8b912de4924d4254421"

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
				transitions[fromType][toType] /= numTransitions
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
	def __init__(self, docModel):
		self.docModel = docModel
		self.sentences = self.docModel.cleanSentences()
		self.fullText = " \n".join(self.sentences)
		self.textRazor = TextRazor(api_key=thomasKey, extractors=["entities", "topics", "words", "dependency-trees"])
		self.nerResults = self.textRazor.analyze(self.fullText)
		self.allEntities = self.nerResults.entities()
		self.matrixIndices = self.getMatrixIndices()
		self.numUniqueEntities = len(self.matrixIndices)
		self.grid = self.fillMatrix()

	def makeEmptyMatrix(self):
		numpyMatrix = list()
		for sentence in self.nerResults.sentences:
			numpyMatrix.append(numpy.zeros(self.numUniqueEntities))
		return numpyMatrix

	def setEntityUseType(self, entityId, matrix, sNum, score):
		matrix[sNum][self.matrixIndices[entityId]] = max(score, matrix[sNum][self.matrixIndices[entityId]])

	def fillMatrix(self):
		matrix = self.makeEmptyMatrix()
		sNum = 0
		for sentence in self.nerResults.sentences:
			for word in sentence.words:
				if "NN" in word.part_of_speech and len(word.entities) > 0:
					entityId = self.getLongestEntity(word.entities)
					if word.relation_to_parent == "nsubj":  # _john_ eats snails
						self.setEntityUseType(entityId, matrix, sNum, subjectScore)
					elif word.relation_to_parent == "xsubj":  # _john_ likes to eat snails
						self.setEntityUseType(entityId, matrix, sNum, subjectScore)
					elif word.relation_to_parent == "nsubjpass":  # _john_ is eaten by bill
						self.setEntityUseType(entityId, matrix, sNum, subjectScore)
					elif word.relation_to_parent == "agent":  # bill was killed by _john_
						self.setEntityUseType(entityId, matrix, sNum, objectScore)
					elif word.relation_to_parent == "dobj":  # bill eats _john_
						self.setEntityUseType(entityId, matrix, sNum, objectScore)
					elif word.relation_to_parent == "pobj":  # john eats with _bill_
						self.setEntityUseType(entityId, matrix, sNum, obliqueScore)
					elif word.relation_to_parent == "npadvmod":  # john is 65 _years_ old
						self.setEntityUseType(entityId, matrix, sNum, obliqueScore)
					elif word.relation_to_parent == "iobj":  # john gave _bill_ flowers
						self.setEntityUseType(entityId, matrix, sNum, obliqueScore)
					elif word.relation_to_parent == "nn":  # _army_ boots are sexy
						pass

					# print "[" + entityId + "]" + str(self.tokenFromScore(matrix[sNum][self.matrixIndices[entityId]]))
			sNum += 1
		return matrix

	def getMatrixIndices(self):
		matrixIndices = {}
		i = 0
		for entity in self.allEntities:
			if entity.id not in matrixIndices.keys():
				matrixIndices[entity.id] = i
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