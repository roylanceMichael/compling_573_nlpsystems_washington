__author__ = 'thomas'
"""
  Python Source Code for ling573 Deliverable 2: Basic Summarizer
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
from evaluate.rougeEvaluator import RougeEvaluator
import extract
import extract.topicReader
import extract.documentRepository
import coreference.rules
import model.doc_model
import kmeans.kMeans

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
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, summaryOutputPath, modelSummaryCachePath)

##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
	return model.doc_model.Doc_Model(docData)


##############################################################
# summarize
##############################################################
def summarize(docModels):
    summary = ""
    kMeansInstance = kmeans.kMeans.KMeans(docModels)

    maxCount = 5
    number = 0
    for topParagraph in kMeansInstance.buildDistances():
        if number > maxCount:
            break
        summary += str(topParagraph[0])
        number += 1

    return summary


##############################################################
# evaluate our summary with rouge
##############################################################
def evaluate():
	return rouge.evaluate()


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

# cache the model summaries
rouge.cacheModelSummaries(topics)

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

for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "processing topicId: " + transformedTopicId
	# let's get all the documents associated with this topic
	models = list()
	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		print "processing docNo: " + foundDocument.docNo
		convertedModel = getModel(foundDocument)
		# updatedCorefModel = coreference.rules.Rules.updateDocumentWithCoreferences(convertedModel)
		models.append(convertedModel)

	# make a summary of the topic cluster
	print topic.category + " : " + topic.title + " : building summary for " + str(len(models)) + " models"
	summary = summarize(models)
	if summary is not None:
		summaryFileName = summaryOutputPath + "/" + transformedTopicId + ".OURS"
		summaryFile = open(summaryFileName, 'w')
		summaryFile.write(summary)
		summaryFile.close()

	print summary

# run rouge evaluator
print "running the rouge evaluator"
evaluation = evaluate()
print evaluation
evaluationFileName = evaluationOutputPath + "/FinalEvaluation.txt"
print evaluationFileName
evaluationFile = open(evaluationFileName, 'w')
evaluationFile.write(evaluation)
evaluationFile.close()
