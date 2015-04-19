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
import model.docModel

# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--doc-input-path2', help='Path to secondary data files', dest='docInputPath2')
parser.add_argument('--topic-xml', help='Path to topic xml file', dest='topicXml')
parser.add_argument('--summary-output-path', help='Path to our generated summaries', dest='summaryOutputPath')
parser.add_argument('--rouge-path', help='Path to rouge', dest='rougePath')
parser.add_argument('--gold-standard-summary-path', help='Path to gold standard summaries', dest='goldStandardSummaryPath')
parser.add_argument('--evaluation-output-path', help='Path to save evaluations', dest='evaluationOutputPath')
args = parser.parse_args()

##############################################################
# global variables
##############################################################
rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, args.summaryOutputPath)

##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
    return model.docModel.DocModel(docData)


##############################################################
# summarize
##############################################################
def summarize(docModels):
    summary = ""
    for docModel in docModels:
        summary += docModel.body[0].full + "\n"
    return summary


##############################################################
# evaluate our summary with rouge
##############################################################
def evaluate(summary):
    #evaluator = RougeEvaluator(args.rougePath, args.summaryOutputPath,
    #                           args.goldStandardSummaryPath, args.evaluationOutputPath)
    #return evaluator.evaluate(summary)
    return "testEvaluation"


##############################################################
# Script Starts Here
###############################################################

# get training xml file
# go through each topic
topics = []
for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
    topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository(args.docInputPath, args.docInputPath2, topics)

for topic in topics:
    # let's get all the documents associated with this topic
    models = list()
    # get the doc objects, and build doc models from them
    for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
        models.append(getModel(foundDocument))

    # make a summary of the topic cluster
    summary = summarize(models)
    if summary is not None:
        summaryFileName = args.summaryOutputPath + "/" + topic.docsetAId + ".OURS"
        summaryFile = open(summaryFileName, 'w')
        summaryFile.write(summary)
        summaryFile.close()

    print topic.category + " : " + topic.title + " : building summary for " + str(len(models)) + " models"
    print summary

    # run rouge evaluator
    evaluation = rouge.evaluate(topic.docsetAId)
    evaluationFileName = args.evaluationOutputPath + "/" + topic.docsetAId

