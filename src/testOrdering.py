__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  Checks how well the Barzilay and Lapata (2005) entity-based coherence ranking algorithm works.

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
from model.entityGrid import EntityGrid
from model.entityGrid import FeatureVector
from model.entityGrid import DummyDocModel
import nltk
import nltk.data
import svmlight

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


def getFullTextAsSentencesFromDocModel(document):
	sentences = []
	for paragraph in document.paragraphs:
		cleanP = paragraph.replace('\n', ' ')
		paragraphSentences = sentence_breaker.tokenize(cleanP)
		sentences.extend(paragraphSentences)

	return sentences

model = svmlight.read_model('my_model.dat')

correct = 0
total = 0
def testDoc(document):
	global total
	global correct

	testVectors = []
	docIndex = 1
	sentences = getFullTextAsSentencesFromDocModel(document)
	if len(sentences) <= 1:  # early return if no transitions.
		return

	goodDoc = DummyDocModel(sentences)
	goodGrid = EntityGrid(goodDoc)
	goodFeatureVector = FeatureVector(goodGrid, docIndex)
	vector = goodFeatureVector.getVector(1)
	testVectors.append(vector)
	#print vector

	for i in range(0, 1):
		badDoc = DummyDocModel(getFullTextAsSentencesFromDocModel(document))
		badDoc.randomizeSentences()
		badGrid = EntityGrid(badDoc)
		badFeatureVector = FeatureVector(badGrid, docIndex)
		vector = badFeatureVector.getVector(1)
		testVectors.append(vector)
		#print vector

	predictions = svmlight.classify(model, testVectors)

	print "predictions for document: " + document.docNo
	for p in predictions:
		print str(p) + " ",
	maxInList = max(predictions)
	total += 1
	if maxInList == predictions[0]:
		correct += 1
		print "\nCORRECT - PercentCorrect: " + str(round(100 * correct / float(total), 2)) + " %\n"
	else:
		print "\nINCORRECT - PercentCorrect: " + str(round(100 * correct / float(total), 2)) + " %\n"



##############################################################
# Script Starts Here
###############################################################
# test with some random permutations of the documents using our model!
print "\n!!!!!!!!!!!!!!!!! TESTING !!!!!!!!!!!!!!!!!!!!!!!!\n"
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
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "caching topicId: " + transformedTopicId
	# let's get all the documents associated with this topic

	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		# print "caching document: " + foundDocument.docNo
		pass

# recache documents for later
# documentRepository.writefileIdDictionaryToFileCache(documentCachePath)
for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "processing topicId: " + transformedTopicId

	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		print "processing docNo: " + foundDocument.docNo
		testDoc(foundDocument)


print "PercentCorrect: " + str(correct / float(total))


