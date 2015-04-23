__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from kmeans.kMeans import KMeans


class SentenceLengthSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		longestSentenceLength = 0

		# get length
		for model in self.docModels:
			for sentence in model.cleanSentences():
				sentenceLength = len(sentence)
				longestSentenceLength = max(sentenceLength, longestSentenceLength)
				self[sentence] = sentenceLength

		# normalize by longest sentence
		longestSentenceLength = float(longestSentenceLength)
		for sentence in self.keys():
			length = self[sentence]
			self[sentence] = length / longestSentenceLength

