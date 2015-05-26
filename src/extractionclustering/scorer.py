__author__ = 'mroylance'

import operator


def handleScoring(allSentences):
	scoreDictionary = {}
	for uniqueSentenceId in allSentences:
		scoreDictionary[uniqueSentenceId] = 0
		compareSentence = allSentences[uniqueSentenceId]

		for otherUniqueSentenceId in allSentences:
			if uniqueSentenceId == otherUniqueSentenceId:
				continue

			score = compareSentence.distanceToOtherSentence(allSentences[otherUniqueSentenceId])
			scoreDictionary[uniqueSentenceId] += score

	for tupleResult in sorted(scoreDictionary.items(), key=operator.itemgetter(1), reverse=True):
		yield tupleResult


def returnTopSentencesFromDifferentClusters(scoredSentenceDictionary, clusters):
	# go through each cluster
	# get the highest scored sentence from it
	# can possibly do two per cluster
	for tupleResult in sorted(scoredSentenceDictionary.items(), key=operator.itemgetter(1), reverse=True):
		yield tupleResult

	# returnSentences = {}
	#
	# for cluster in clusters[0]:
	# 	highestSentence = None
	# 	highestScore = 0
	#
	# 	for pointId in cluster.points:
	# 		point = cluster.points[pointId]
	#
	# 		if point.uid in scoredSentenceDictionary and scoredSentenceDictionary[point.uid] > highestScore:
	# 			highestScore = scoredSentenceDictionary[point.uid]
	# 			highestSentence = point.sentence
	#
	# 	if highestSentence is not None:
	# 		returnSentences[highestSentence] = highestScore
	#
	# for tupleResult in sorted(returnSentences.items(), key=operator.itemgetter(1), reverse=True):
	# 	yield tupleResult