__author__ = 'mroylance'

import uuid

nounPhraseKey = "NP"

class Point:
	def __init__(self, sentence):
		self.sentence = sentence
		self.uid = str(uuid.uuid1())
		self.features = {}

		self.createNpFeatures()

	def createBigramFeatures(self):
		if self.sentence is None:
			return

		previousChunk = None
		for chunk in self.sentence:
			currentChunk = str(chunk).lower()

			if previousChunk == None:
				previousChunk = currentChunk
				continue

			self.features[(previousChunk, currentChunk)] = None

			previousChunk = currentChunk

	def createNpFeatures(self):
		if self.sentence is None:
			return

		for chunk in self.sentence:
			if chunk.tag == nounPhraseKey:
				self.features[str(chunk).lower()] = None

	def createPosFeatures(self):
		if self.sentence is None:
			return

		for chunk in self.sentence:
			self.features[(str(chunk).lower(), chunk.tag)] = None

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

		return score

	def __str__(self):
		return str(self.sentence)
