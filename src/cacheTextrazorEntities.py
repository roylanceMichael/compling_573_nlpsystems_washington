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

def getAllSummaryFileNames():
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

def cacheDoc(document):
	sentences = getFullTextAsSentencesFromDocModel(document)
	textRazorInfo = textrazor.textRazorEntityExtraction.getTextRazorInfo(sentences)
	entities = textRazorInfo.entities()
	trsentences = textRazorInfo.sentences
	docEntityMap[document.docNo] = [entities, trsentences]


def cacheSummary(sentences, fileName):
	textRazorInfo = textrazor.textRazorEntityExtraction.getTextRazorInfo(sentences)
	entities = textRazorInfo.entities()
	trsentences = textRazorInfo.sentences
	summaryEntityMap[fileName] = [entities, trsentences]

def cacheDocumentsFromTopics():
	# test with some random permutations of the documents using our model!
	print "\n!!!!!!!!!!!!!!!!! CACHING ENTITIES !!!!!!!!!!!!!!!!!!!!!!!!\n"
	# get training xml file
	# go through each topic
	topics = []
	for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
		topics.append(topic)

	documentRepository = extract.documentRepository.DocumentRepository(args.docInputPath, args.docInputPath2, topics)

	# load the cached docs
	documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)

	# load and cache the docs if they are not loaded.  just get them if they are.
	for topic in topics:
		print "processing topicId: " + topic.id

		# get the doc objects, and build doc models from them
		for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
			print "processing docNo: " + foundDocument.docNo
			cacheDoc(foundDocument)

def cacheDocumentsFromSummaries():
	files = getAllSummaryFileNames()
	numDocs = len(files)
	startTime = time.time()
	fNumDocs = float(numDocs)
	numDocsProcessed = 1
	maxN = 5000
	for fileName in files:
		sentences = readSentencesFromFile(fileName)

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

cacheDocumentsFromSummaries()
writeAndValidateMaps("summaryEntityMap.pickle", summaryEntityMap)








