__author__ = 'mroylance'

from summaryTechnique import SummaryTechnique
from sentenceDistanceSummaryTechnique import SentenceDistanceSummaryTechnique
from sentenceLengthSummaryTechnique import SentenceLengthSummaryTechnique
from npClusteringTechnique import NpClusteringSummaryTechnique
from tfidfSummaryTechnique import TfidfSummaryTechnique
from matrixSummaryTechnique import MatrixSummaryTechnique
from model.doc_model import Cluster
from matrixSummaryTechnique import MatrixSummaryTechnique

import operator


class InitialSummarizer:
	def __init__(self, docModels, idf, tryTfIdf, tryMatrix, trySentenceDistance, trySentenceLength, tryNpClustering):
		self.docModels = docModels
		self.idf = idf
		self.N = 10  # keep the top N sentences for each technique
		self.wordCount = 100

		self.docCluster = Cluster(docModels, "", "", idf)

		self.techniques = list()
		self.tfIdf = TfidfSummaryTechnique(tryTfIdf, 1.0, self.docCluster)
		self.techniques.append(self.tfIdf)
		self.matrix = MatrixSummaryTechnique(tryMatrix, 1.0, self.docCluster)
		self.techniques.append(self.matrix)
		self.sentenceDistance = SentenceDistanceSummaryTechnique(trySentenceDistance, 1.0, docModels)
		self.techniques.append(self.sentenceDistance)
		self.sentenceLength = SentenceLengthSummaryTechnique(trySentenceLength, 1.0, docModels)
		self.techniques.append(self.sentenceLength)
		self.npClustering = NpClusteringSummaryTechnique(tryNpClustering, 1.0, docModels)
		self.techniques.append(self.npClustering)
		self.summarize()

	def summarize(self):
		for technique in self.techniques:
			if technique.enabled:
				technique.rankSentences()
	
	def getBestSentences(self, w1=None, w2=None, w3=None, w4=None, w5=None):
		if w1 is not None:
			self.tfIdf.weight = w4
		if w2 is not None:
			self.matrix.weight = w1
		if w3 is not None:
			self.sentenceDistance.weight = w2
		if w4 is not None:
			self.sentenceLength.weight = w3
		if w5 is not None:
			self.npClustering.weight = w4

		aggregateSentences = {}
		for model in self.docModels:
			for sentence in model.cleanSentences():
				sum = 0.0
				for technique in self.techniques:
					sum += technique[sentence]
				aggregateSentences[sentence] = sum
		sortedAggregateSentences = sorted(aggregateSentences.items(), key=operator.itemgetter(1), reverse=True)
		#topNSortedAggregateSentences = sortedAggregateSentences[:self.N]  # tuples here... convert to sentences
		#justTopNSentences = [seq[0] for seq in topNSortedAggregateSentences]
		justTopNSentences = [seq[0] for seq in sortedAggregateSentences]
	
		# maximum summary length is measured in words
		summary = ""
		currentWords = 0
		for s in justTopNSentences:
			summary += "\n"
			words = s.split()
			currentWords += len(words)
			if currentWords > self.wordCount:
				continue
			summary += " ".join(words)
	
		return summary.strip()





