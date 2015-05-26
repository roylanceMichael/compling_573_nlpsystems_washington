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
	returnSentences = {}

	print scoredSentenceDictionary

	for cluster in clusters[0]:
		highestSentence = None
		highestScore = 0

		for pointId in cluster.points:
			point = cluster.points[pointId]
			# print point.uid
			# print point.sentence.uuid
			# print (point.sentence.uuid in scoredSentenceDictionary)
			# print (point.uid in scoredSentenceDictionary)
			# for key in scoredSentenceDictionary:
			# 	print key
			# 	if key == point.uid:
			# 		print "FOUND"
			# 	if key == point.sentence.uuid:
			# 		print "FOUND"

			if point.uid in scoredSentenceDictionary and scoredSentenceDictionary[point.uid] > highestScore:
				highestScore = scoredSentenceDictionary[point.uid]
				highestSentence = point.sentence

		if highestSentence is not None:
			returnSentences[highestSentence] = highestScore

	for sentence in returnSentences:
		yield sentence