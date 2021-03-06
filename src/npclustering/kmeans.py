__author__ = 'mroylance'

import point
import cluster
import random



# def buildPointForEachSentence(docModels):
# 	for docModel in docModels:
# 		for paragraph in docModel.paragraphs:
# 			for sentence in paragraph:
# 				yield point.Point(sentence)


def getInitialKPoints(points, k):
	# just grabbing a random initial point, for now
	initialPoints = [points[0]]

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


def performKMeans(initialPoints, points, minimumMovement=0, maxIterations=100):
	if len(initialPoints) == 0:
		return None

	clusters = []

	i = 1
	for initialPoint in initialPoints:

		if initialPoint in points:
			points.remove(initialPoint)

		newCluster = cluster.Cluster(i)
		newCluster.addPoint(initialPoint)
		clusters.append(newCluster)
		i += 1

	rebalanceClusters(clusters)

	# add all points to first cluster
	currentMovement = 5000
	iterationNumber = 0

	while currentMovement > minimumMovement and iterationNumber < maxIterations:
		currentMovement = 0

		for point in points:
			highestScore = 0
			mostSimilarCluster = None
			currentCluster = None

			for actualCluster in clusters:
				if point.uid in actualCluster.points:
					currentCluster = actualCluster
					mostSimilarCluster = actualCluster

			for actualCluster in clusters:
				score = actualCluster.calculateSimilarity(point)

				if score > highestScore:
					highestScore = score
					mostSimilarCluster = actualCluster

			hasClusterAlready = currentCluster is not None

			if hasClusterAlready and currentCluster.number == mostSimilarCluster.number:
				continue

			if hasClusterAlready:
				currentCluster.removePoint(point)

			if mostSimilarCluster is not None:
				mostSimilarCluster.addPoint(point)
				currentMovement += 1

		rebalanceClusters(clusters)

		print "done with iteration #" + str(iterationNumber) + " with " + str(currentMovement) + " movements"
		iterationNumber += 1

	if iterationNumber > maxIterations:
		return (clusters, iterationNumber)

	return (clusters, iterationNumber)

def rebalanceClusters(clusters):
	for actualCluster in clusters:
		actualCluster.recalculateFeatures()