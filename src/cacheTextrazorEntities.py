__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  Caches entities for all documents using textrazor.

  This code does the following:
  1. runs through each doc file
  2. makes a random-ordered doc
  3. classifies for rank
  4. checks to see accuracy



"""

import argparse

import extract
import extract.topicReader
import extract.documentRepository
import model.idf
import textrazor.textRazorEntityExtraction
import nltk
import nltk.data
import svmlight
import pickle
import os
import time

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
docEntityMap = {}
summaryEntityMap = {}


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


def getFullTextAsSentencesFromDocModel(document):
	sentences = []
	for paragraph in document.paragraphs:
		cleanP = paragraph.replace('\n', ' ')
		paragraphSentences = sentence_breaker.tokenize(cleanP)
		sentences.extend(paragraphSentences)

	return sentences

devtestFilePath = "/opt/dropbox/14-15/573/Data/peers/devtest"
trainingFilePath = "/opt/dropbox/14-15/573/Data/peers/training"

def getSummaryFileNames(directory):
	# directories = [devtestFilePath, trainingFilePath]
	fileNames = []
	# for directory in directories:

	files = os.listdir(directory)
	for file in files:
		fileNames.append(os.path.join(directory, file))

	for fileName in fileNames:
		print fileName
	return fileNames


def cacheDoc(document):
	sentences = getFullTextAsSentencesFromDocModel(document)
	textRazorInfo = textrazor.textRazorEntityExtraction.getTextRazorInfo(sentences)
	entities = textRazorInfo.entities()
	trsentences = textRazorInfo.sentences
	docEntityMap[document.docNo] = [entities, trsentences]

def getEntityIdsFromTREntities(trEntities):
	entities = []
	for entity in trEntities:
		entities.append(entity.id)
	return entities

def cacheSummary(sentences, fileName):
	textRazorInfo = textrazor.textRazorEntityExtraction.getTextRazorInfo(sentences)
	entities = getEntityIdsFromTREntities(textRazorInfo.entities())
	trsentences = textRazorInfo.sentences
	summaryEntityMap[fileName] = [entities, trsentences]



def cacheDocumentsFromSummaries(directory):
	global summaryEntityMap
	summaryEntityMap = {}
	files = getSummaryFileNames(directory)
	numDocs = len(files)
	startTime = time.time()
	fNumDocs = float(numDocs)
	numDocsProcessed = 1

	for fileName in files:
		sentences = readSentencesFromFile(fileName)
		if len(sentences) > 0:
			# get the doc objects, and build doc models from them
			secs = time.time() - startTime
			docsPerSec = numDocsProcessed / secs
			print "processing doc(" + str(numDocsProcessed) + "/" + str(numDocs) + "): " + fileName + ", rate=" + str(round(docsPerSec, 4)) + " docs per second."
			cacheSummary(sentences, fileName)
		numDocsProcessed += 1



def writeAndValidateMaps(mapFileName, writeMap):
	print "Map created, caching..."

	pickleFileName = os.path.join("../cache/textrazorCache", mapFileName)
	pickleFile = open(pickleFileName, 'wb')
	pickle.dump(writeMap, pickleFile, pickle.HIGHEST_PROTOCOL)

	print "Finished caching %d documents" % len(writeMap)

	pickleFile = open(pickleFileName, 'rb')
	readMap = pickle.load(pickleFile)

	print "Validating cache:  read %d documents" % len(readMap)


##############################################################
# Script Starts Here
###############################################################
#cacheDocumentsFromTopics()
#writeAndValidateMaps("docEntityMap.pickle", docEntityMap)

# cacheDocumentsFromSummaries(devtestFilePath)
# writeAndValidateMaps("devtestEntityMap.pickle", summaryEntityMap)

cacheDocumentsFromSummaries(trainingFilePath)
writeAndValidateMaps("trainingEntityMap.pickle", summaryEntityMap)









