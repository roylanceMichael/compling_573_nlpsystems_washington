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
from extract import document

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
def extract(docBuffer):
    # call here into Michael's reader
    return document.Document.factory(docBuffer)


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


# main loop
files = glob.glob(args.docInputPath)
for filePath in files:
    docBuffer = ""
    docName = ""
    dataFile = open(filePath, "r")
    for line in dataFile:
        # read file
        if line == "<DOC>\n":
            docBuffer = line
            line = dataFile.next
            while line != "</DOC>\n":
                docBuffer += line
                line = dataFile.next
            docBuffer += line
        # now process
        docData = extract(docBuffer)
        docModel = getModel(docData)
        summary = summarize(docModel)
        # save our summary
        outputFileName = args.summaryOutputPath + "/" + summary[0]
        outputFile = open(outpufFileName, "w")
        outputFile.write(summary)
        evaluation = evaluate(summary)
    close(filePath)