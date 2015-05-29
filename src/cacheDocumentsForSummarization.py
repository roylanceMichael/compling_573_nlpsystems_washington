__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 3: Ordering Summarizer
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 5/16/2015

  This code does the following:
  1. opens doc files
  2. extracts data from doc files
  3. summarizes doc files and outputs summaries for each topic
  4. compares summary to baseline using ROUGE and outputs results

"""

import argparse
import extract
import extract.topicReader
import extract.documentRepository2




# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--topic-xml', help='Path to topic xml file', dest='topicXml')
parser.add_argument('--data-type', help='one of: \"devtest\", \"training\", or \"evaltest\"', dest='dataType')

args = parser.parse_args()

##############################################################
# global variables
##############################################################
documentCachePath = "../cache/documentCache"




##############################################################
# Script Starts Here
###############################################################

# get training xml file
# go through each topic
topics = []
for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
	topics.append(topic)

documentRepository = extract.documentRepository2.DocumentRepository2(args.docInputPath, args.dataType, topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)


# load and cache the docs if they are not loaded.  just get them if they are.
for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "caching topicId: " + transformedTopicId
	# let's get all the documents associated with this topic

	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		documentRepository.writefileIdDictionaryToFileCache(documentCachePath)

# recache documents for later
# documentRepository.writefileIdDictionaryToFileCache(documentCachePath)
print "done caching documents"
