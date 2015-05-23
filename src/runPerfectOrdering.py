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
import re
import os
import os.path
import extract
import extract.topicReader
import extract.documentRepository

from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare


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
# helper function for printing out buffers to files
##############################################################
def writeBufferToFile(path, buffer):
	outFile = open(path, 'w')
	outFile.write(buffer)
	outFile.close()

##############################################################
# global variables
##############################################################
summaryOutputPath = args.outputPath
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"

rouge = RougeEvaluator(args.rougePath, args.goldStandardSummaryPath, summaryOutputPath, modelSummaryCachePath, rougeCacheDir)

topics = []
for topic in extract.topicReader.Topic.factoryMultiple(args.topicXml):
	topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository(args.docInputPath, args.docInputPath2, topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)

# cache the model summaries
rouge.cacheModelSummaries(topics)

summaries = {}
for fileName in os.listdir(args.goldStandardSummaryPath):
	filePath = os.path.join(args.goldStandardSummaryPath, fileName)

	outputFileName = fileName[0:5] + fileName[len(fileName)-1]

	with open(filePath, 'r') as docFile:
		entireContent = docFile.read()
		summaries[outputFileName] = entireContent

for summaryId in summaries:
	summaryFileName = summaryOutputPath + "/" + summaryId
	summaryFile = open(summaryFileName, 'w')
	summaryFile.write(summaries[summaryId])
	summaryFile.close()

	print summaries[summaryId]
	print "----------"

print "running the rouge evaluator"
evaluationResults = rouge.evaluate()
evaluation = evaluationResults[0]
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results"), evaluation)

# call the evaluation comparison routine.
# note:  this will only print the summaries you have on your machine.
# 		 i.e. you should have run the meadSummaryGenerator.py first
# 		 (though defaults are checked into git)
comparator = EvaluationCompare(evaluationOutputPath, meadCacheDir, rouge)
comparison = comparator.getComparison()
print "\n" + comparison
writeBufferToFile(os.path.join(evaluationOutputPath, "results_compare.txt"), comparison)