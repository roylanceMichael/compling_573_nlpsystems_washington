__author__ = 'mroylance'

class Point:
	def __init__(self, sentence):
		self.sentence = sentence
		self.features = sentence.chunkDict
		self.uid = sentence.uuid

	def calculateSimilarity(self, otherPoint):
		# union over intersection

		score = 0
		combinedFeatures = {}
		for feature in self.features:
			combinedFeatures[feature] = None

		for feature in otherPoint.features:
			combinedFeatures[feature] = None

		for feature in combinedFeatures:
			if feature in otherPoint.features and feature not in self.features:
				score += 1
			if feature not in otherPoint.features and feature in self.features:
				score += 1

		return score / float(len(self.features) + len(otherPoint.features) + 1)

	def __str__(self):
		return str(self.sentence)

