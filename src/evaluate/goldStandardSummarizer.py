__author__ = 'thomas'
"""
  Execute Gold Standard Summarization

  Python Source Code for ling573 Deliverable 2: Basic Summarizer
  Author: Thomas Marsh
  Team: Thomas Marsh, Brandon Gaylor, Michael Roylance
  Date: 4/12/2015

  This code does the following:
  1. opens doc files
  2. extracts data from doc files
  3. summarizes doc files
 


"""

import argparse
import re
import nltk
import glob

# get parser args and set up global variables
parser = argparse.ArgumentParser(description='\"First 10\" Document Summarizer.')
parser.add_argument('inputPath', nargs=1, help='Path to data files')
parser.add_argument('outputPath', nargs=1, help='Path to gold standard summary files')
args = parser.parse_args()

namePattern = re.compile("<DOCNO> (.+) </DOCNO>")

##############################################################
# write the first ten lines to a file
##############################################################
def writeBuffer(docName, docBuffer):
	docFileName = args.outputPath[0] + "/" + docName + ".First10.txt"
	sentences = nltk.tokenize.sent_tokenize(docBuffer)

	numSentences = min([9, len(sentences) - 1])

	if numSentences == 0:
		return

	outFile = open(docFileName, "w")

	for i in range(0, numSentences):
		sentence = sentences[i].replace("\n", "").strip()
		outFile.write(sentence + "\n")

	outFile.close()


##############################################################
# get data from each <DOC> element
##############################################################
def extract(fileName):
	file = open(fileName, 'r')
	docBuffer = ""
	docName = ""
	for line in file:
		if line == "</DOC>\n":
			writeBuffer(docName, docBuffer)
			docBuffer = ""
			docName = ""
		else:
			result = namePattern.findall(line)
			if len(result) != 0:
				docName = result[0]
			elif line == "<P>\n":
				line = file.next()
				while line != "</P>\n":
					docBuffer += " " + line
					line = file.next()


##############################################################
# Script Starts Here
###############################################################
# main loop
files = glob.glob(args.inputPath[0])
for filePath in files:
	extract(filePath)

