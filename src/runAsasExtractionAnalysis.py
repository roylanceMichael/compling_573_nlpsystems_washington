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
import argparse
from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare



# from compress import compress
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--doc-input-path2', help='Path to data files', nargs='?', default=None, dest='docInputPath2')
parser.add_argument('--topic-xml', help='Path to topic xml file', dest='topicXml')
parser.add_argument('--gold-standard-summary-path', help='Path to gold standard summaries',
					dest='modelSummaryDir')
parser.add_argument('--data-type', help='one of: \"devtest\", \"training\", or \"evaltest\"', nargs='?',
					default="devtest", dest='dataType')
args = parser.parse_args()

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
rougeDir = "/opt/dropbox/14-15/573/code/ROUGE"


rankModel = svmlight.read_model('../cache/svmlightCache/svmlightModel.dat')

rouge = RougeEvaluator(rougeDir,
                      	args.modelSummaryDir,
                    	summaryOutputPath,
                       	modelSummaryCachePath,
					   	rougeCacheDir)

totalClusters = 25
minimumAverageClusterRange = 30
maximumAverageClusterRange = 55
maxWords = 130
topics = []
topicTitles = {}
for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
	topics.append(topic)
	topicTitles[topic.id] = re.sub("\s+", " ", topic.title)

documentRepository = extract.documentRepository.DocumentRepository(args.docInputPath, args.docInputPath2,
                                                                   args.dataType, topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)

# cache the model summaries
rouge.cacheModelSummaries(topics)


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
			goldTopicDocModels[topicId][fileName] = goldDocModel
		else:
			goldTopicDocModels[topicId] = {fileName: goldDocModel}

goldSentences = {}
for topicId in goldTopicDocModels:
	allSentences = extractionclustering.sentence.factory(goldTopicDocModels[topicId], {})
	goldSentences[topicId] = allSentences

# fileName refers to cache/asasCache/D1001A ...
for fileName in os.listdir(cachePath):
	# grab the topic dictionary with docModels inside of it
	pickleFilePath = os.path.join(cachePath, fileName)

	# open
	if os.path.exists(pickleFilePath):
		pickleFile = open(pickleFilePath, 'rb')
		topicDictionary = pickle.load(pickleFile)
		topicTitle = ""
		if fileName in topicTitles:
			topicTitle = topicTitles[fileName].lower().strip()

		topicTitleDict = {}
		for word in topicTitle.split(" "):
			topicTitleDict[word] = None

		foundGoldSentences = {}
		if fileName in goldSentences:
			foundGoldSentences = goldSentences[fileName]

		# all the cached sentences from the topic
		allSentences = extractionclustering.sentence.factory(topicDictionary, topicTitleDict, foundGoldSentences)

		print "doing clustering now on summarization... with " + str(len(foundGoldSentences)) + " gold sentences"

		scoredSentenceDictionary = {}
		for tupleResult in extractionclustering.scorer.handleScoring(allSentences):
			key = tupleResult[0]
			scoredSentenceDictionary[key] = (allSentences[key], tupleResult[1])

		allPoints = []
		# let's try from 20 - 30
		averageClusterSize = 0
		currentClusterSize = 20
		while currentClusterSize < 30:
			allPoints = []
			for sentenceId in allSentences:
				allPoints.append(extractionclustering.point.Point(allSentences[sentenceId]))
			initialPoints = npclustering.kmeans.getInitialKPoints(allPoints, currentClusterSize)
			clusters = npclustering.kmeans.performKMeans(initialPoints, allPoints)

			runningClusterSize = 0

			for cluster in clusters[0]:
				runningClusterSize += len(cluster.points)

			averageClusterSize = runningClusterSize / float(len(cluster.points))

			print "cluster sizes: " + str(averageClusterSize)

			if minimumAverageClusterRange < averageClusterSize < maximumAverageClusterRange:
				break

			currentClusterSize += 1

		clusterSizes[fileName] = averageClusterSize

		# wordCount = 0
		# uniqueSummaries = {}
		# bestSentences = []
		# for tupleResult in extractionclustering.scorer.handleScoring(allSentences):
		# 	print tupleResult
		# 	if wordCount > maxWords:
		# 		break
		#
		# 	sentence = allSentences[tupleResult[0]]
		# 	bestSentences.append(sentence)
		#
		# 	if sentence.simple in uniqueSummaries:
		# 		continue
		#
		# 	uniqueSummaries[sentence.simple] = None
		#
		# 	wordSize = len(sentence.simple.split(" "))
		# 	wordCount += wordSize

		wordCount = 0
		uniqueSummaries = {}
		bestSentences = []
		for topSentenceResult in extractionclustering.scorer.returnTopSentencesFromDifferentClusters(
				scoredSentenceDictionary, clusters):
			if wordCount > maxWords:
				break

			sentence = topSentenceResult[0]
			# sentence = compress(sentence)
			bestSentences.append(sentence)

			if sentence.simple in uniqueSummaries:
				continue

			uniqueSummaries[sentence.simple] = None

			wordSize = len(sentence.simple.split(" "))
			wordCount += wordSize

		summary = ""
		for uniqueSentence in uniqueSummaries:
			summary += uniqueSentence + "\n"

		print summary
		if summary is not None:
			summaryFileName = summaryOutputPath + "/" + fileName
			summaryFile = open(summaryFileName, 'wb')
			summaryFile.write(summary)
			summaryFile.close()

		print "now calculating the best order..."

		# bestOrder = getBestSummaryOrder(bestSentences, docIndex)
		#
		# summary = ""
		# uniqueSummaries = {}
		# for newSentence in bestOrder:
		# 	actualText = re.sub("\s+", " ", newSentence.simple) + "\n"
		# 	if actualText not in uniqueSummaries:
		# 		uniqueSummaries[actualText] = None
		# 		summary += actualText

		if summary is not None:
			summaryFileName = reorderedSummaryOutputPath + "/" + fileName
			summaryFile = open(summaryFileName, 'wb')
			summaryFile.write(summary)
			summaryFile.close()

		print summary

	docIndex += 1

print "running the rouge evaluator"
evaluationResults = rouge.evaluate()
evaluation = evaluationResults[0]
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results"), evaluation)
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results_reordered"), evaluation)

# call the evaluation comparison routine.
# note:  this will only print t
# he summaries you have on your machine.
# 		 i.e. you should have run the meadSummaryGenerator.py first
# 		 (though defaults are checked into git)
comparator = EvaluationCompare(evaluationOutputPath, meadCacheDir, rouge)
comparison = comparator.getComparison()
print "\n" + comparison
writeBufferToFile(os.path.join(evaluationOutputPath, "results_compare.txt"), comparison)

print "average cluster sizes"
summedAverage = 0
for fileName in clusterSizes:
	# print fileName + ": " + str(clusterSizes[fileName])
	summedAverage += clusterSizes[fileName]

print "average overall: " + str(summedAverage / float(len(clusterSizes)))


