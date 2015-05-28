__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  Implements something similar to Barzilay and Lapata (2005)'s entity-based coherence ranking
  algorithm to reorder sentences in summaries

  This code does the following:
  1. reads each output summary
  2. decodes with ranking decoder using previously generated model
  	 (model generation/training is done with entityCoherenceTrainer.py)
  3. rewrites summaries using new ordering
  4. compares: (a) unordered summaries (b) reordered summaries (c) baseline summaries.


"""

import argparse
import svmlight
import os
import itertools

import nltk
import nltk.data

import extract
import extract.topicReader
import extract.documentRepository
from entitygrid.textrazorEntityGrid import TextrazorEntityGrid
from entitygrid.entityGrid import FeatureVector
from entitygrid.entityGrid import DummyDocModel
from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare




# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--doc-input-path2', help='Path to secondary data files', dest='docInputPath2')
parser.add_argument('--topic-xml', help='Path to topic xml file', dest='topicXml')
parser.add_argument('--output-path', help='Path to our output', dest='outputPath')
parser.add_argument('--rouge-path', help='Path to rouge', dest='rougePath')
parser.add_argument('--gold-standard-summary-path', help='Path to gold standard summaries',
					dest='goldStandardSummaryPath')
args = parser.parse_args()

##############################################################
# global variables
##############################################################
summaryOutputPath = args.outputPath
reorderedSummaryOutputPath = args.outputPath + "_reordered"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
rankModel = svmlight.read_model('../cache/svmlightCache/svmlightModel.dat')

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"




##############################################################
# helper function for printing out buffers to files
##############################################################
def writeBufferToFile(path, buffer):
	outFile = open(path, 'w')
	outFile.write(buffer)
	outFile.close()


def readSentencesFromFile(fileName):
	allSentences = []
	inFile = open(fileName, 'r')
	for line in inFile:
		allSentences.append(line.strip())
	inFile.close()
	return allSentences


def writeSentencesToFile(sentences, fileName):
	file = open(fileName, 'w')
	for sentence in sentences:
		file.write(sentence + "\n")
	file.close()

def getPlaintextSentencesFromTextrazorSentences(sentences):
	rawSentences = []

	for sentence in sentences:
		noSpaceOnNextWord = True
		rawSentence = ""
		for word in sentence.words:
			if word.relation_to_parent == "punct":
				if word.token == "-LRB-":
					rawSentence += " ("
					noSpaceOnNextWord = True
				elif word.token == "-RRB-":
					rawSentence += ")"
				else:
					rawSentence += word.token
			else:
				if not noSpaceOnNextWord and not word.token[0] == '\'':
					rawSentence += " " + word.token
				else:
					noSpaceOnNextWord = False
					rawSentence += word.token
		rawSentences.append(rawSentence)
	return rawSentences

def getBestSummaryOrder(sentences, fileName, docIndex, numDocs):
	permList = []

	testVectors = []

	doc = DummyDocModel(sentences)
	grid = TextrazorEntityGrid(doc.cleanSentences(), 2)
	textrazorSentences = grid.textrazorSentences
	permutations = [perm for perm in itertools.permutations(textrazorSentences)]
	print "numPermutations: " + str(len(permutations))
	for permutation in permutations:
		grid.textrazorSentences = permutation
		grid.buildMatrix()
		permList.append(permutation)
		featureVector = FeatureVector(grid, docIndex)
		vector = featureVector.getVector(1)
		testVectors.append(vector)
		# grid.printMatrix()
		# featureVector.printVector()

	predictions = svmlight.classify(rankModel, testVectors)

	for p in predictions:
		print str(p) + " ",

	maxInList = max(predictions)
	maxIndex = predictions.index(maxInList)
	print "\nreordering document(" + str(docIndex) + "/" + str(numDocs) + "): " + fileName + ", best permutation index=" + str(maxIndex)
	bestOrder = getPlaintextSentencesFromTextrazorSentences(permList[maxIndex])
	return bestOrder


#####################################################################################
# script starts here
#####################################################################################
# copy all the files over.
files = os.listdir(summaryOutputPath)
docIndex = 1
for fileName in files:
	sentences = readSentencesFromFile(os.path.join(summaryOutputPath, fileName))
	if len(sentences) > 1:
		bestOrder = getBestSummaryOrder(sentences, fileName, docIndex, len(files))
		writeSentencesToFile(bestOrder, os.path.join(reorderedSummaryOutputPath, fileName))
	else:
		writeSentencesToFile(sentences, os.path.join(reorderedSummaryOutputPath, fileName))
	docIndex += 1



print "running the rouge evaluator"
rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, summaryOutputPath, modelSummaryCachePath, rougeCacheDir)
# get training xml file
# go through each topic
topics = []
for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
	topics.append(topic)
rouge.cacheModelSummaries(topics)
evaluationResults = rouge.evaluate()
evaluation = evaluationResults[0]
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results"), evaluation)


# now switch to reordered output
rouge2 = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, reorderedSummaryOutputPath, modelSummaryCachePath, rougeCacheDir)
rouge2.rougeConfigFileName = os.path.join(rouge2.rougeCachePath, "rouge_config_reordered.xml")
rouge2.cacheModelSummaries(topics)
evaluationResults = rouge2.evaluate()
evaluation = evaluationResults[0]
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results_reordered"), evaluation)



# call the evaluation comparison routine.
# note:  this will only print the summaries you have on your machine.
# 		 i.e. you should have run the meadSummaryGenerator.py and reorderSummaries.py first
# 		 (though defaults are checked into git)
comparator = EvaluationCompare(evaluationOutputPath, meadCacheDir, rouge)
comparison = comparator.getComparison()
print "\n" + comparison
writeBufferToFile(os.path.join(evaluationOutputPath, "results_compare.txt"), comparison)
