__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  Trainer for my implementation of Barzilay and Lapata (2005) entity-based coherence ranking algorithm

  This code does the following:
  1. reads through corpus
  2. builds entity grid, and computes a ranking feature vector for each input document
  3. trains a model using svmlight
  3. writes model to file



"""

import random
import argparse
import cPickle
import svmlight
import time
import os

import nltk
import nltk.data
import glob

import model.idf
from entitygrid.textrazorEntityGrid import TextrazorEntityGrid
from entitygrid.entityGrid import FeatureVector
from entitygrid.entityGrid import DummyDocModel



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
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
idf = model.idf.Idf(idfCachePath)


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
		tline = line.strip()
		if len(tline) != 0 and tline is not None:
			allSentences.append(line.strip())
	inFile.close()
	return allSentences

def writeSentencesToFile(sentences, fileName):
	file = open(fileName, 'w')
	for sentence in sentences:
		file.write(sentence + "\n")
	file.close()


def getSentencesFromCorpusDocument(document):
	sentences = []
	cleanDoc = document.replace('\n', ' ')
	paragraphSentences = sentence_breaker.tokenize(cleanDoc)
	sentences.extend(paragraphSentences)
	return sentences

def getFullTextAsSentencesFromDocModel(document):
	sentences = []
	for paragraph in document.paragraphs:
		cleanP = paragraph.replace('\n', ' ')
		paragraphSentences = sentence_breaker.tokenize(cleanP)
		sentences.extend(paragraphSentences)

	return sentences

##############################################################
# Script Starts Here
###############################################################


docIndex = 1
featureVectors = []
firstDocument = None


devtestEntityMapFileName = "../cache/textrazorCache/devtestEntityMap.pickle"
devtestEntityMap = {}
trainingEntityMapFileName = "../cache/textrazorCache/trainingEntityMap.pickle"
trainingEntityMap = {}
fileNameDictionary = {}
devtestScoresFilePath = "/opt/dropbox/14-15/573/Data/scores/devtest.manual.peer.A"
trainingScoresFilePath = "/opt/dropbox/14-15/573/Data/scores/training.manual.peer.A"
devtestFilePath = "/opt/dropbox/14-15/573/Data/peers/devtest"
trainingFilePath = "/opt/dropbox/14-15/573/Data/peers/training"

numDocs = 0

def loadFromPickleFile(pickleFileName):
	print "Loading entities from " + pickleFileName
	begin = time.time()
	try:
		pickleFile = open(pickleFileName, 'rb')
		data = cPickle.load(pickleFile)
		loadTime = time.time() - begin
		print "Finished loading entities from " + pickleFileName + " in " + str(loadTime) + "sec"
		return data
	except IOError:
		return None

def addToFileNameDictionary(cluster, fileName, qualityScore, responsivenessScore, pickleFileName):
	global numDocs
	numDocs += 1
	try:
		fileNameDictionary[cluster][fileName] = [qualityScore, responsivenessScore, pickleFileName]
	except KeyError:
		fileNameDictionary[cluster] = {}
		fileNameDictionary[cluster][fileName] = [qualityScore, responsivenessScore, pickleFileName]
	print "[%d] %s %d" % (numDocs, fileName, qualityScore)

def getFileNameFromClusterId(clusterId, fileNumber, annotator, baseFilePath):
	fileName = "%s.M.100.%s.%d" % (clusterId, annotator, fileNumber)
	return fileName

def addConstraintsFromFileToDictionary(constraintFileName, baseFilePath):
	constraintFile = open(constraintFileName, "r")

	for line in constraintFile:
		items = line.split()
		clusterId = items[0]
		fileNumber = int(items[1])
		annotator = items[5]
		qualityScore = int(items[8])
		responsivenessScore = int(items[9])
		fileName = getFileNameFromClusterId(clusterId, fileNumber, annotator, baseFilePath)
		fullFileName = os.path.join(baseFilePath, fileName)
		pickleFileName = os.path.join("../cache/textrazorCache", fileName)
		addToFileNameDictionary(clusterId, fullFileName, qualityScore, responsivenessScore, pickleFileName)

	constraintFile.close()


def loadConstraintDictionary():
	addConstraintsFromFileToDictionary(devtestScoresFilePath, devtestFilePath)
	addConstraintsFromFileToDictionary(trainingScoresFilePath, trainingFilePath)


def getSentenceText(sentences):
	plainSentences = []
	for sentence in sentences:
		plainSentences.append(" ".join(sentence))
	return plainSentences


loadConstraintDictionary()


startTime = time.time()
fNumDocs = float(numDocs)
numDocsTried = 1
#maxN = 5000
clusterIndex = 1
for cluster in fileNameDictionary:
	for fileName in fileNameDictionary[cluster]:
		qualityScore = fileNameDictionary[cluster][fileName][0]
		responsivenessScore = fileNameDictionary[cluster][fileName][1]
		pickleFileName = fileNameDictionary[cluster][fileName][2]
		textRazorInfo = loadFromPickleFile(pickleFileName)  # (fileName, entities, sentences)
		if textRazorInfo is not None:
			sentences = readSentencesFromFile(fileName)

			try:
				textrazorEntities = textRazorInfo[1]
				textrazorSentences = textRazorInfo[2]
			except KeyError:
				textrazorEntities = None
				textrazorSentences = None

			# get the doc objects, and build doc models from them
			secs = time.time() - startTime
			docsPerSec = numDocsTried / secs
			print "processing doc(" + str(numDocsTried) + "/" + str(numDocs) + "): " + fileName + ", rate=" + str(round(docsPerSec, 4)) + " docs per second."
			nskipped = 1
			if len(sentences) > 1:  # because there have to be transitions
				docModel = DummyDocModel(sentences)
				grid = TextrazorEntityGrid(docModel.cleanSentences(), 2, textrazorEntities, textrazorSentences)
				if grid.valid and len(grid.matrixIndices) > 0:
					grid.printMatrix()
					featureVector = FeatureVector(grid, clusterIndex)
					featureVector.printVector()
					featureVector.printVectorWithIndices()
					vector = featureVector.getVector(qualityScore)
					featureVectors.append(vector)
					docIndex += 1

			else:
				print "SKIPPING (not enough sentences) %s, nskipped=(%d)" % (fileName, nskipped)
				nskipped += 1
		else:
			print "SKIPPING (no pickle file)%s, nskipped=(%d)" % (fileName, nskipped)
			nskipped += 1

		# pickleFile = open("../cache/svmlightCache/featureVectors.pickle", 'wb')
		# pickle.dump(featureVectors, pickleFile, pickle.HIGHEST_PROTOCOL)
		# pickleFile.close()
		# if docIndex >= maxN:
		#	break
		numDocsTried += 1
	clusterIndex += 1
# now train on the data
model = svmlight.learn(featureVectors, type='ranking', verbosity=0)
svmlight.write_model(model, '../cache/svmlightCache/svmlightModel.dat')
