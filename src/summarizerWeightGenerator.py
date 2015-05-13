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
import model.idf
import model.doc_model
import npclustering.npClustering
import summarization.initialSummarizer
from order.order import in_order
from realize.simple_realize import simple_realize
from summarization.initialSummarizer import InitialSummarizer
import numpy



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
idfCachePath = "../cache/idfCache"

rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, summaryOutputPath, modelSummaryCachePath)
idf = model.idf.Idf(idfCachePath)


##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
	return model.doc_model.Doc_Model(docData)



def kMeansSentences(docModels, maxCount):
	number = 0
	kMeansInstance = npclustering.npClustering.NpClustering(docModels)
	for topParagraph in kMeansInstance.buildDistances():
		if number > maxCount:
			break
		for sentence in topParagraph[0]:
			yield sentence

		number += 1


##############################################################
# evaluate our summary with rouge
##############################################################
def evaluate():
	return rouge.evaluate()


##############################################################
# print out models
##############################################################
def printSummary(docModels):
	for docModel in docModels:
		for paragraph in docModel.paragraphs:
			print str(paragraph)


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


def summarizeAndGetWeights(models, w1, w2, w3, w4, w5):
	# make a summary of the topic cluster
	initialSummarizer = InitialSummarizer(models, idf, True, True, True)
	summary = initialSummarizer.getBestSentences(w1, w3, w4)
	if summary is not None:
		summaryFileName = summaryOutputPath + "/" + topic.id
		summaryFile = open(summaryFileName, 'w')
		summaryFile.write(summary)
		summaryFile.close()

	evaluationResults = evaluate()
	evaluationDict = evaluationResults[1]
	rouge2precision = evaluationDict['rouge_2_precision']
	rouge2recall = evaluationDict['rouge_2_recall']
	rouge2fscore = evaluationDict['rouge_2_f_score']

	# for technique in initialSummarizer.techniques:
	#	print technique.techniqueName + ": " + str(technique.weight) + ", enabled: " + str(technique.enabled)
	l = [w1, w2, w3, w4, w5, rouge2precision, rouge2recall, rouge2fscore]
	# print l
	return l


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


	weightsMatrixArray = []



	resultsArray = summarizeAndGetWeights(models, 1.0, 0.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.0, 1.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.0, 0.0, 1.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.0, 0.0, 0.0, 1.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.0, 0.0, 0.0, 0.0, 1.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 1.0, 1.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.25, 1.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.5, 1.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 0.75, 1.0, 0.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 1.0, 1.0, 1.0, 1.0, 1.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 1.0, 1.0, 1.0, 1.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 1.0, 1.0, 1.0, 0.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	resultsArray = summarizeAndGetWeights(models, 1.0, 1.0, 0.0, 1.0, 0.0)
	print resultsArray
	weightsMatrixArray.append(resultsArray)

	# inc = 0.25
	# w1 = 0.0
	# while w1 <= 1.0:
	# 	w2 = 0.0
	# 	while w2 <= 1.1:
	# 		w3 = 0.0
	# 		while w3 <= 1.1:
	# 			w4 = 0.0
	# 			while w4 <= 1.1:
	# 				if not (w1 == 0.0 and w2 == 0.0 and w3 == 0.0 and w4 == 0.0):
	# 					resultsArray = summarizeAndGetWeights(models, 0.0, w2, w3, w4)
	# 					print resultsArray
	# 					weightsMatrixArray.append(resultsArray)
	# 				w4 += inc
	# 			w3 += inc
	# 		w2 += inc
	# 	w1 += inc


	# get max average
	max = 0.0
	maxRow = None
	for matrixRow in weightsMatrixArray:
		sum = matrixRow[5] + matrixRow[6] + matrixRow[7]
		ave = sum / 3.0
		if ave > max:
			max = ave
			maxRow = matrixRow

	print "Max Row:"
	print maxRow