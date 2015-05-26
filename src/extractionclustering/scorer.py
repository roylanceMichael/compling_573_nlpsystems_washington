__author__ = 'mroylance'

import re
import operator

def handleScoring(allSentences):
	scoreDictionary = {}
	for uniqueSentenceId in allSentences:
		scoreDictionary[uniqueSentenceId] = 0
		compareSentence = allSentences[uniqueSentenceId]

		#for keywordResult in compareSentence.keywordResults:
		# print compareSentence.simple
		# print "-------------------------"
		for otherUniqueSentenceId in allSentences:
			if uniqueSentenceId == otherUniqueSentenceId:
				continue

			score = compareSentence.distanceToOtherSentence(allSentences[otherUniqueSentenceId])
			scoreDictionary[uniqueSentenceId] += score

	maxWords = 100
	wordCount = 0
	uniqueSummaries = {}
	bestSentences = []
	for tupleResult in sorted(scoreDictionary.items(), key=operator.itemgetter(1), reverse=True):
		yield tupleResult