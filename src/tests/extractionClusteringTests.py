__author__ = 'mroylance'

import re
import unittest
import pickle
import extract.topicReader
import extract.document
import extractionclustering.sentence
import extractionclustering.kmeans
import extractionclustering.scorer
import extractionclustering.point
import npclustering.npClustering
import npclustering.kmeans

fileName = "D1001A"
cacheTopicPath = "../cache/asasCache/" + fileName
topicTitles = {}

def cacheTopicTitles():
	for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
		topicTitles[topic.id] = re.sub("\s+", " ", topic.title)


class ExtractionClusteringTests(unittest.TestCase):
	def test_parseSingleDocument(self):
		# arrange
		if len(topicTitles) == 0:
			cacheTopicTitles()

		pickleFile = open(cacheTopicPath, 'rb')
		topicDictionary = pickle.load(pickleFile)
		topicTitle = topicTitles[fileName].lower().strip()

		topicTitleDict = {}
		for word in topicTitle.split(" "):
			topicTitleDict[word] = None

		allSentences = extractionclustering.sentence.factory(topicDictionary, topicTitleDict)

		scoredSentenceDictionary = {}
		for tupleResult in extractionclustering.scorer.handleScoring(allSentences):
			key = tupleResult[0]
			scoredSentenceDictionary[key] = (allSentences[key], tupleResult[1])

		# similarity stuff
		# clustering stuff
		allPoints = []
		for sentenceId in allSentences:
			allPoints.append(extractionclustering.point.Point(allSentences[sentenceId]))

		initialPoints = npclustering.kmeans.getInitialKPoints(allPoints, 20)

		clusters = npclustering.kmeans.performKMeans(initialPoints, allPoints)

		maxWords = 100
		wordCount = 0
		uniqueSummaries = {}
		bestSentences = []
		for topSentenceResult in extractionclustering.scorer.returnTopSentencesFromDifferentClusters(scoredSentenceDictionary, clusters):
			if wordCount > maxWords:
				break

			print topSentenceResult
			sentence = topSentenceResult[0]
			bestSentences.append(sentence)

			if sentence.simple in uniqueSummaries:
				continue

			uniqueSummaries[sentence.simple] = None

			wordSize = len(sentence.simple.split(" "))
			wordCount += wordSize

		for summary in uniqueSummaries:
			print summary

		# act
		for cluster in clusters[0]:
			print "----------CLUSTER " + str(cluster.number) + " SIZE (" + str(len(cluster.points)) + ")"
			clusterSummary = ""
			iterNum = 0
			for pointKey in cluster.points:

				if iterNum > 5:
					break

				clusterSummary = clusterSummary + cluster.points[pointKey].sentence.simple + " \n"
				iterNum += 1

			print clusterSummary
			print "highest is: " + cluster.highestScoringPoint().sentence.simple

		self.assertTrue(True)