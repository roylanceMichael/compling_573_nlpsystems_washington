__author__ = 'mroylance'

import random

def getInitialKPoints(points, k):
	# just grabbing a random initial point, for now
	initialPoints = [random.choice(points)]

	while len(initialPoints) < k:
		largestScore = 0
		largestPoint = None

		for point in points:
			totalPointScore = 0
			for initialPoint in initialPoints:
				totalPointScore += initialPoint.calculateSimilarity(point)

			if largestScore < totalPointScore:
				largestScore = totalPointScore
				largestPoint = point

		initialPoints.append(largestPoint)

	return initialPoints