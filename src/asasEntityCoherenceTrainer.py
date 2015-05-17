__author__ = 'mroylance'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 4/12/2015

  Trainer for my implementation of Barzilay and Lapata (2005) entity-based coherence ranking algorithm

  This code does the following:
  1. reads through corpus
  2. builds entity grid, and computes a ranking feature vector for each input document
  3. trains a model using svmlight
  3. writes model to file



"""

import argparse
import pickle

import extract
import extract.topicReader
import extract.documentRepository
import model.idf
from model.entityGrid import EntityGrid
from model.entityGrid import FeatureVector
from model.entityGrid import DummyDocModel
import nltk
import nltk.data
import svmlight
from nltk.corpus import reuters
import time
import os

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

# recache documents for later
# documentRepository.writefileIdDictionaryToFileCache(documentCachePath)
docIndex = 1
featureVectors = []
firstDocument = None


def getAllFileNames():
	directories = ["/opt/dropbox/14-15/573/Data/models/devtest",
				   "/opt/dropbox/14-15/573/Data/models/training/2009",
				   "/opt/dropbox/14-15/573/Data/mydata"]
	fileNames = []
	for directory in directories:
		files = os.listdir(directory)
		for file in files:
			fileNames.append(os.path.join(directory, file))

	for fileName in fileNames:
		print fileName
	return fileNames


def getSentenceText(sentences):
	plainSentences = []
	for sentence in sentences:
		plainSentences.append(" ".join(sentence))
	return plainSentences

files = getAllFileNames()
numDocs = len(files)
startTime = time.time()
fNumDocs = float(numDocs)
numDocsTried = 1
maxN = 5000
for fileName in files:
	sentences = readSentencesFromFile(fileName)

	# get the doc objects, and build doc models from them
	secs = time.time() - startTime
	docsPerSec = numDocsTried / secs
	print "processing doc(" + str(docIndex) + "/" + str(numDocsTried) + "): " + fileName + ", rate=" + str(round(docsPerSec, 4)) + " docs per second."

	if len(sentences) > 1:  # because there have to be transitions
		docModel = DummyDocModel(sentences)
		grid = EntityGrid(docModel)
		if len(grid.matrixIndices) > 0:
			# grid.printMatrix()
			featureVector = FeatureVector(grid, docIndex)
			# featureVector.printVector()
			# featureVector.printVectorWithIndices()
			vector = featureVector.getVector(2)

			docModel.randomizeSentences()
			badGrid = EntityGrid(docModel)
			# grid.printMatrix()
			badFeatureVector = FeatureVector(badGrid, docIndex)
			# featureVector.printVector()
			# featureVector.printVectorWithIndices()
			vector = featureVector.getVector(2)
			badVector = badFeatureVector.getVector(1)
			print vector
			print badVector
			featureVectors.append(vector)
			featureVectors.append(badVector)
			docIndex += 1

	pickleFile = open("../cache/svmlightCache/featureVectors.pickle", 'wb')
	pickle.dump(featureVectors, pickleFile, pickle.HIGHEST_PROTOCOL)
	pickleFile.close()
	if docIndex >= maxN:
		break
	numDocsTried += 1

# now train on the data
model = svmlight.learn(featureVectors, type='ranking', verbosity=0)
svmlight.write_model(model, '../cache/svmlightCache/svmlightModel.dat')
