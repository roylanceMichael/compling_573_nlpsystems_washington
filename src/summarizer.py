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

# get parser args and set up global variables
parser = argparse.ArgumentParser(description='Basic Document Summarizer.')
parser.add_argument('--doc-input-path', help='Path to data files', dest='docInputPath')
parser.add_argument('--rouge-path', help='Path to rouge', dest='rougePath')
parser.add_argument('--gold-standard-summary-path', help='Path to gold standard summaries', dest='goldStandardSummaryPath')
parser.add_argument('--summaryOutputPath', help='Path to our generated summaries', dest='summaryOutputPath')
parser.add_argument('--evaluation-output-path', help='Path to save evaluations', dest='evaluationOutputPath')
args = parser.parse_args()



##############################################################
# global variables
##############################################################



##############################################################
# read a data file
##############################################################
def extract(fileName):
    # call here into Michael's reader
    # docExtractor = docExtractor.DocExtractor()
    # return docExtractor.extract(filename)
    return ["input data1", "input data2"]


##############################################################
# send the data to the model generator
##############################################################
def getModel(docData):
    # create brandon's model class
    # return docModel.DocModel(docData)
    return ["doc data1", "doc data2"]


##############################################################
# summarize
##############################################################
def summarize(docModel):
    # summarizer = summarizer.Summarizer()
    # return summarizer.summarize(docModel)

    return "Kenneth Joseph Lenihan, a New York research" + \
           "sociologist who helped refine the scientific methods used in" + \
           "criminology, died May 25 at his home in Manhattan"


##############################################################
# evaluate our summary with rouge
##############################################################
def evaluate(summary):
    evaluator = RougeEvaluator(args.rougePath, args.summaryOutputPath,
                               args.goldStandardSummaryPath, args.evaluationOutputPath)
    return evaluator.evaluate(summary)


##############################################################
# Script Starts Here
###############################################################


# main loop
files = glob.glob(args.docInputPath)
for filePath in files:
    docDataArray = extract(filePath)
    for docData in docDataArray:
        docModel = getModel(docData)
        summary = summarize(docModel)
        evaluation = evaluate(summary)
