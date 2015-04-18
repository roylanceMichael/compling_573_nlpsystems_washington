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

import glob
import argparse
from evaluate.rougeEvaluator import RougeEvaluator
import extract
import extract.topicReader
import extract.documentRepository
from extract import document

# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--doc-input-path2', help='Path to secondary data files', dest='docInputPath2')
parser.add_argument('--topic-xml', help='Path to topic xml file', dest='topicXml')
parser.add_argument('--rouge-path', help='Path to rouge', dest='rougePath')
parser.add_argument('--gold-standard-summary-path', help='Path to gold standard summaries', dest='goldStandardSummaryPath')
parser.add_argument('--summaryOutputPath', help='Path to our generated summaries', dest='summaryOutputPath')
parser.add_argument('--evaluation-output-path', help='Path to save evaluations', dest='evaluationOutputPath')
args = parser.parse_args()



##############################################################
# global variables
##############################################################


##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
    return [docData.docNo, docData.paragraphs[0]]

##############################################################
# summarize
##############################################################
def summarize(docModel):
    return docModel


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
  allSummarizedModels = []
  for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
    initialModel = getModel(foundDocument)
    summarizeModel = summarize(initialModel)
    if summarizeModel != None:
      allSummarizedModels.append(summarizeModel)

  print topic.category + " : " + topic.title +  " : building summary for " + str(len(allSummarizedModels)) + " models"
  print "this is when we will print out a summarization of the models"