__author__ = 'mroylance'


class Cluster:
	def __init__(self, number):
		self.number = number
		self.points = {}
		self.currentFeatures = {}

	def addPoint(self, point):
		self.points[point.uid] = point

	def removePoint(self, point):
		self.points.pop(point.uid, None)

	def recalculateFeatures(self):
		self.currentFeatures = {}
		for pointKey in self.points:
			for feature in self.points[pointKey].features:
				if feature in self.currentFeatures:
					self.currentFeatures[feature] += 1
				else:
					self.currentFeatures[feature] = 1

	def calculateSimilarity(self, otherPoint):
		# union over intersection
		score = 0

		for feature in otherPoint.features:
			if feature in self.currentFeatures:
				score += self.currentFeatures[feature]

		return score / float(len(self.currentFeatures) + len(otherPoint.features) + 1)

	def highestScoringPoint(self):
		highestPoint = None
		highestScore = 0

		for pointKey in self.points:
			score = self.calculateSimilarity(self.points[pointKey])
			if score > highestScore:
				highestPoint = self.points[pointKey]
				highestScore = score

		return highestPoint

	def __str__(self):
		return str(self.number)