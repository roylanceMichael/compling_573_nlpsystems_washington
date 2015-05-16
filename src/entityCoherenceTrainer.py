__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Summarizer with Ordering
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 4/12/2015

  This code does the following:
  1. opens a doc files
  2. extracts data from doc files
  3. summarizes doc files
  4. compares summary using ROUGE and outputs results


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

##############################################################
# Script Starts Here
###############################################################

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
docIndex = 1
featureVectors = []
firstDocument = None
for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "processing topicId: " + transformedTopicId
	# let's get all the documents associated with this topic
	models = list()
	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		if firstDocument is None:
			firstDocument = foundDocument
		print "processing docNo: " + foundDocument.docNo

		sentences = getFullTextAsSentencesFromDocModel(foundDocument)
		if len(sentences) > 1:  # because there have to be transitions
			grid = EntityGrid(DummyDocModel(sentences))
			# grid.printMatrix()
			featureVector = FeatureVector(grid, docIndex)
			# featureVector.printVector()
			# featureVector.printVectorWithIndices()
			vector = featureVector.getVector(2)


			badDoc = DummyDocModel(getFullTextAsSentencesFromDocModel(foundDocument))
			badDoc.randomizeSentences()
			badGrid = EntityGrid(badDoc)
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

# now train on the data
model = svmlight.learn(featureVectors, type='ranking', verbosity=0)
svmlight.write_model(model, 'my_model.dat')


# now test with some random permutations of the first document using our model!
print "\n!!!!!!!!!!!!!!!!! TESTING !!!!!!!!!!!!!!!!!!!!!!!!\n"
testVectors = []
docIndex = 1
goodDoc = DummyDocModel(getFullTextAsSentencesFromDocModel(firstDocument))
goodGrid = EntityGrid(goodDoc)
goodFeatureVector = FeatureVector(goodGrid, docIndex)
vector = goodFeatureVector.getVector(2)
testVectors.append(vector)
print vector

for i in range(0, 5):
	badDoc = DummyDocModel(getFullTextAsSentencesFromDocModel(firstDocument))
	badDoc.randomizeSentences()
	badGrid = EntityGrid(badDoc)
	badFeatureVector = FeatureVector(badGrid, docIndex)
	vector = badFeatureVector.getVector(1)
	testVectors.append(vector)
	print vector

predictions = svmlight.classify(model, testVectors)

for p in predictions:
	print p

