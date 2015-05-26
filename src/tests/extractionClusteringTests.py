__author__ = 'mroylance'

import re
import unittest
import pickle
import extract.document
import extractionclustering.sentence
import model.doc_model
import npclustering.npClustering
import npclustering.kmeans

fileName = "D1001A"
cacheTopicPath = "../cache/asasCache/" + fileName
topicTitles = {}

def cacheTopicTitles():
	for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
		topicTitles[topic.id] = re.sub("\s+", " ", topic.title)



class KmeansTests(unittest.TestCase):
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

		allSentences = extractionclustering.sentence.factory()

		foundDocument = extract.document.Document.factory(docXml)
		otherFoundDocument = extract.document.Document.factory(otherDocXml)
		docModel = model.doc_model.Doc_Model(foundDocument)
		otherDocModel = model.doc_model.Doc_Model(otherFoundDocument)

		allPoints = []

		for point in npclustering.kmeans.buildPointForEachSentence([docModel, otherDocModel]):
			allPoints.append(point)

		initialPoints = npclustering.kmeans.getInitialKPoints(allPoints, 3)

		clusters = npclustering.kmeans.performKMeans(initialPoints, allPoints)

		# act
		for cluster in clusters[0]:
			print "----------CLUSTER " + str(cluster.number) + " SIZE (" + str(len(cluster.points)) + ")"
			print cluster.currentFeatures
			for pointKey in cluster.points:
				print cluster.points[pointKey]
				print " "

			print "highest is:"
			print cluster.highestScoringPoint().sentence

		self.assertTrue(True)