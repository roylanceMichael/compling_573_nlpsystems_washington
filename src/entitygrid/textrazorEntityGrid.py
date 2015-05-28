__author__ = 'thomas'

from textrazor import textRazorEntityExtraction
from entitygrid import entityGrid
from entitygrid.entityGrid import EntityGrid



class TextrazorEntityGrid(EntityGrid):
	# build entity grid
	def __init__(self, sentences, minNumEntityMentions=1, entityIds=None, textrazorSentences=None):
		EntityGrid.__init__(self, sentences, minNumEntityMentions)

		if entityIds is None or textrazorSentences is None:
			nerResults = textRazorEntityExtraction.getTextRazorInfo(self.sentences)
			self.textrazorSentences = nerResults.sentences
			self.matrixIndices = self.getMatrixIndices(self.getEntityIdsFromTextrazorEntities(nerResults.entities()))
		else:
			self.matrixIndices = self.getMatrixIndices(entityIds)
			self.textrazorSentences = textrazorSentences

		self.originalMatrixIndices = self.matrixIndices
		# HACKERY WARNING:
		# ugh!  this sets the sentences to textrazor's sentences instead of the original sentences,
		# just in case there is a discrepency between the number of sentences
		# need a better way to handle this!
		self.originalSentences = self.sentences
		self.sentences = self.textrazorSentences
		self.numSentences = len(self.textrazorSentences)  # just to make sure they agree
		self.buildMatrix()

	def buildMatrix(self):
		self.matrixIndices = self.originalMatrixIndices
		self.grid = self.fillMatrix()
		self.originalMatrixIndices = self.matrixIndices
		self.compressMatrix()

	def fillMatrix(self):
		matrix = self.makeEmptyMatrix(len(self.matrixIndices))
		sNum = 0
		for sentence in self.textrazorSentences:
			for word in sentence.words:
				if "NN" in word.part_of_speech and len(word.entities) > 0:
					entityId = self.getLongestEntity(word.entities)
					if word.relation_to_parent == "nsubj":  # _john_ eats snails
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.subjectScore)
					elif word.relation_to_parent == "xsubj":  # _john_ likes to eat snails
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.subjectScore)
					elif word.relation_to_parent == "nsubjpass":  # _john_ is eaten by bill
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.subjectScore)
					elif word.relation_to_parent == "agent":  # bill was killed by _john_
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.objectScore)
					elif word.relation_to_parent == "dobj":  # bill eats _john_
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.objectScore)
					elif word.relation_to_parent == "pobj":  # john eats with _bill_
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.obliqueScore)
					elif word.relation_to_parent == "npadvmod":  # john is 65 _years_ old
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.obliqueScore)
					elif word.relation_to_parent == "iobj":  # john gave _bill_ flowers
						self.setEntityUseType(entityId, matrix, sNum, entityGrid.obliqueScore)
					elif word.relation_to_parent == "nn":  # _army_ boots are sexy
						pass

					# print "[" + entityId + "]" + str(self.tokenFromScore(matrix[sNum][self.matrixIndices[entityId]]))
			sNum += 1
		return matrix

	def getEntityIdsFromTextrazorEntities(self, textrazorEntities):
		entityIds = set()
		for entity in textrazorEntities:
			if entity not in entityIds:
				entityIds.add(entity.id)
		return entityIds

	@staticmethod
	def getLongestEntity(entities):
		longestLen = 0
		longestEntity = None
		for entity in entities:
			if len(entity.matched_words) > longestLen:
				longestLen = len
				longestEntity = entity.id
		return longestEntity

