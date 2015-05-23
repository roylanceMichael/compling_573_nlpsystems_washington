__author__ = 'mroylance'

import operator
import re
from summaryTechnique import SummaryTechnique

nounPhraseKey = "NP"

class HighestFrequencyTechnique(SummaryTechnique):
	def rankSentences(self, parameters):
		self.docModels.processNPs()
		frequencyDict = {}

		for docModel in self.docModels:
			for paragraph in docModel.paragraphs:
				for sentence in paragraph:
					previousChunk = None
					for chunk in sentence:
						currentChunk = str(chunk).lower()
						if not re.match("[A-Za-z]+", currentChunk) or chunk.tag != nounPhraseKey:
							continue

						if previousChunk is None:
							previousChunk = currentChunk
							continue

						compareTuple = (previousChunk, currentChunk)

						if compareTuple in frequencyDict:
							frequencyDict[compareTuple] += 1
						else:
							frequencyDict[compareTuple] = 1

		words = 0
		summary = ""
		for tupleResult in sorted(frequencyDict.items(), key=operator.itemgetter(1), reverse=True):
			i = 0
			while i < tupleResult[1]:
				summary = summary + str(tupleResult[0][0]) + " " + str(tupleResult[0][1]) + " " 
				i += 1
				words += 2

			if words > 100:
				break

		print "current summary: " + summary
		self[summary] = 1
