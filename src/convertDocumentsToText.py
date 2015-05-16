__author__ = 'mroylance'

import os
import sys
import extract
import attensity.semantic_server
import model.doc_model
import extract.topicReader
import extract.documentRepository
import coherence.scorer
import coreference.rules
import pickle

rootDirectory = "/Users/mroylance/tempDocuments"

topics = []
for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
	topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository("/corpora/LDC/LDC02T31/", "/corpora/LDC/LDC08T25/data/", topics)

# load and cache the docs if they are not loaded.  just get them if they are.
docModelCache = {}
for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "caching topicId: " + transformedTopicId
	# let's get all the documents associated with this topic

	topicFolder = rootDirectory + "/" + topic.id
	if not os.path.exists(topicFolder):
		os.makedirs(topicFolder)

	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		filePath = topicFolder + "/" + foundDocument.docNo
		paragraphs = ""
		for paragraph in foundDocument.paragraphs:
			paragraphs += paragraph

		with open(filePath, "w") as textFile:
			textFile.write(paragraphs)