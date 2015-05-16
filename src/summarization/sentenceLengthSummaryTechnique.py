__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from npclustering.npClustering import NpClustering


class SentenceLengthSummaryTechnique(SummaryTechnique):
	def rankSentences(self, paramaters):
		longestSentenceLength = 0

		tempDict = {}
		# get length
		for model in self.docModels:
			for sentence in model.cleanSentences():
				sentenceLength = len(sentence)
				longestSentenceLength = max(sentenceLength, longestSentenceLength)
				tempDict[sentence] = sentenceLength

		# normalize by longest sentence
		longestSentenceLength = float(longestSentenceLength)
		for sentence in tempDict.keys():
			length = tempDict[sentence]
			self[sentence] = length / longestSentenceLength

