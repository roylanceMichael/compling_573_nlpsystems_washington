__author__ = 'thomas'
"""
  Python Source Code for ling573:  make summaries using mead summarizer
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 4/12/2015

  This code does the following:
  1. opens doc files
  2. extracts data from doc files
  3. summarizes doc files using mead
  4. compares summary using ROUGE and outputs results


"""

import argparse

from evaluate.rougeEvaluator import RougeEvaluator
import extract
import extract.topicReader
import extract.documentRepository
import model.idf
import model.doc_model
import coreference.rules
from mead import meadDocumentCluster
from mead import meadDocument
from mead import meadSummarizer
import os





# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Mead Summarizer.')
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
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadDocumentCachePath = "../cache/meadCache/docClusters"
meadEvaluationCachePath = "../cache/meadCache/evaluations"
meadSummaryCachePath = "../cache/meadCache/summaries"
meadPath = "../mead/bin"
rougeCachePath = "../cache/rougeCache"


idf = model.idf.Idf(idfCachePath)
rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, meadSummaryCachePath, modelSummaryCachePath, rougeCachePath)

##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
	initialModel = model.doc_model.Doc_Model(docData)
	coreference.rules.updateDocumentWithCoreferences(initialModel)
	return initialModel


##############################################################
# print out models
##############################################################
def printSummary(docModels):
	for docModel in docModels:
		for paragraph in docModel.paragraphs:
			print str(paragraph)



def evalAndWrite(summaryOutputPath, label):
	rouge.reset()
	rouge.systemSummaryDir = os.path.abspath(summaryOutputPath)
	rouge.rougeConfigFileName = os.path.join(rougeCachePath, "rouge_config_mead_" + label + ".xml")
	# cache the model summaries
	rouge.cacheModelSummaries(topics)

	evalResults = rouge.evaluate()
	evaluation = evalResults[0]
	evalOutputFilePath = os.path.join(meadEvaluationCachePath, label + ".results")
	evalFile = open(evalOutputFilePath, 'w')
	evalFile.write(evaluation)
	evalFile.close()




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
documentRepository.writefileIdDictionaryToFileCache(documentCachePath)

meadStandardSummarizer = meadSummarizer.MeadSummarizer(meadPath, meadSummaryCachePath, meadDocumentCachePath, "standard")
meadInitialSummarizer = meadSummarizer.MeadSummarizer(meadPath, meadSummaryCachePath, meadDocumentCachePath, "initial")
meadRandomSummarizer = meadSummarizer.MeadSummarizer(meadPath, meadSummaryCachePath, meadDocumentCachePath, "random")

for topic in topics:
	id = topic.id.strip()
	print "processing topicId: " + id
	# let's get all the documents associated with this topic
	# get the doc objects, and build doc models from them
	docCluster = meadDocumentCluster.MeadDocumentCluster(topic)
	docCluster.write(meadDocumentCachePath)

	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		meadDoc = meadDocument.MeadDocument(topic, foundDocument)
		meadDoc.write(meadDocumentCachePath)
		print "processing docNo: " + foundDocument.docNo

	meadStandardSummarizer.summarizeAndWrite(id)
	meadInitialSummarizer.summarizeAndWrite(id)
	meadRandomSummarizer.summarizeAndWrite(id)


evalAndWrite(meadStandardSummarizer.outputPath, "standard")
evalAndWrite(meadInitialSummarizer.outputPath, "initial")
evalAndWrite(meadRandomSummarizer.outputPath, "random")

