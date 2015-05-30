__author__ = 'mroylance'

"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  Extracts entities and other data using attensity parser

  This code does the following:
  1. reads through documents
  2. uncaches entity and semantic information from pickle files
  	 (cached with cacheDocumentsWithExtractions.py)
  3. extracts entities for documents and runs coherence experiments

"""

import os
import re
import itertools
import pickle

import svmlight
import extract
import extract.topicReader
import extract.documentRepository
import entitygrid.asasEntityGrid
import npclustering.kmeans
import extractionclustering.kmeans
import extractionclustering.scorer
import extractionclustering.point
import extractionclustering.sentence
from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare

from compress import compress

cachePath = "../cache/asasCache"
goldCachePath = "../cache/asasGoldCache"
summaryOutputPath = "../outputs"
reorderedSummaryOutputPath = summaryOutputPath + "_reordered"
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"



totalClusters = 25
minimumAverageClusterRange = 30
maximumAverageClusterRange = 55
topics = []
topicTitles = {}
for topic in extract.topicReader.Topic.factoryMultiple("/opt/dropbox/14-15/573/Data/Documents/evaltest/GuidedSumm11_test_topics.xml"):
	topics.append(topic)
	topicTitles[topic.id] = re.sub("\s+", " ", topic.title)

documentRepository = extract.documentRepository.DocumentRepository("/corpora/LDC/LDC11T07/data/", None,
                                                                   "evaltest", topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)



def getBestSummaryOrder(sentences, docIndex):
	permList = []

	testVectors = []

	permutations = itertools.permutations(sentences)
	for permutation in permutations:
		permList.append(permutation)
		grid = entitygrid.asasEntityGrid.AsasEntityGrid(permutation)
		featureVector = entitygrid.entityGrid.FeatureVector(grid, docIndex)
		vector = featureVector.getVector(1)
		testVectors.append(vector)

	predictions = svmlight.classify(rankModel, testVectors)

	maxInList = max(predictions)
	maxIndex = predictions.index(maxInList)
	print "reordering document(" + str(docIndex) + ")"
	bestOrder = permList[maxIndex]
	return bestOrder


##############################################################
# helper function for printing out buffers to files
##############################################################
def writeBufferToFile(path, buffer):
	outFile = open(path, 'w')
	outFile.write(buffer)
	outFile.close()


docIndex = 0

domainOfKeywordTypes = {}

clusterSizes = {}

# fileName refers to cache/asasGoldCache/D0901-A.M.100.A.A ...
goldTopicDocModels = {}
for fileName in os.listdir(goldCachePath):
	# grab the pickled gold summary
	pickleFilePath = os.path.join(goldCachePath, fileName)

	if os.path.exists(pickleFilePath):
		pickleFile = open(pickleFilePath, 'rb')
		goldDocModel = pickle.load(pickleFile)

		# get corresponding topicId
		topicId = fileName[0:5] + fileName[len(fileName)-3:len(fileName)-2]

		if topicId in goldTopicDocModels:
			goldTopicDocModels[topicId][topicId] = goldDocModel
		else:
			goldTopicDocModels[topicId] = {topicId: goldDocModel}

goldSentences = {}
for topicId in goldTopicDocModels:
	allSentences = extractionclustering.sentence.factory(goldTopicDocModels[topicId], {})
	goldSentences[topicId] = allSentences


num_sentences = 3

# fileName refers to cache/asasCache/D1001A ...
for fileName in os.listdir(cachePath)[:1]:
	# grab the topic dictionary with docModels inside of it
	pickleFilePath = os.path.join(cachePath, fileName)

	# open
	if os.path.exists(pickleFilePath):
		pickleFile = open(pickleFilePath, 'rb')
		topicDictionary = pickle.load(pickleFile)

		topicTitleDict = {}

		# all the cached sentences from the topic
		allSentences = extractionclustering.sentence.factory(topicDictionary, topicTitleDict, goldSentences[fileName])
		if num_sentences:
			for sentenceId in allSentences:
				if num_sentences:
					#this is where I am testing the compressor
					s = allSentences[sentenceId]
					print s.simple
					c = compress(s)
					print(c.simple)
					print("")
					num_sentences -= 1

	docIndex += 1