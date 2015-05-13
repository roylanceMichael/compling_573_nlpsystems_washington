__author__ = 'mroylance'

from summaryTechnique import SummaryTechnique
from sentenceDistanceSummaryTechnique import SentenceDistanceSummaryTechnique
from sentenceLengthSummaryTechnique import SentenceLengthSummaryTechnique
from npClusteringTechnique import NpClusteringSummaryTechnique
from tfidfSummaryTechnique import TfidfSummaryTechnique
from graphSummaryTechnique import GraphSummaryTechnique
from model.doc_model import Cluster
from graphSummaryTechnique import GraphSummaryTechnique

import operator


class InitialSummarizer:
	def __init__(self, docModels, idf, tryTfIdf, trySentenceDistance, trySentenceLength):
		self.docModels = docModels
		self.idf = idf
		self.N = 10  # keep the top N sentences for each technique
		self.wordCount = 100

		self.docCluster = Cluster(docModels, "", "", idf)

		self.techniques = list()
		self.tfIdf = TfidfSummaryTechnique(tryTfIdf, 1.0, self.docCluster, "tf-idf")
		self.techniques.append(self.tfIdf)
		self.sentenceDistance = SentenceDistanceSummaryTechnique(trySentenceDistance, 1.0, docModels, "sdist")
		self.techniques.append(self.sentenceDistance)
		self.sentenceLength = SentenceLengthSummaryTechnique(trySentenceLength, 1.0, docModels, "slen")
		self.techniques.append(self.sentenceLength)
		self.summarize()

	def summarize(self):
		for technique in self.techniques:
			if technique.enabled:
				technique.rankSentences()
	
	def getBestSentences(self, w_tfidf=None, w_sd=None, w_sl=None, w_cosign=None, w_np=None):
		if w_tfidf is not None:
			self.tfIdf.weight = w_tfidf
		if w_sd is not None:
			self.sentenceDistance.weight = w_sd
		if w_sl is not None:
			self.sentenceLength.weight = w_sl

		aggregateSentences = {}
		for model in self.docModels:
			for sentence in model.cleanSentences():
				sum = 0.0
				for technique in self.techniques:
					res = technique[sentence]
					#print sentence
					#print "technique: " + technique.techniqueName + ", score: " + str(res) + ", sentence: " + sentence
					sum += res
				aggregateSentences[sentence] = sum

		# feed aggregate scores to graph so it can handle overlap
		graphweight = 2.0 if not w_cosign else w_cosign + w_np
		cosignweight = 0.5 if not w_cosign else w_cosign / (w_cosign + w_np)
		self.graph = GraphSummaryTechnique(True, graphweight, self.docCluster, "cosign+np", cosignweight, independentweights=aggregateSentences)
		self.graph.rankSentences()

		sortedAggregateSentences = sorted(self.graph.items(), key=operator.itemgetter(1), reverse=True)
		#topNSortedAggregateSentences = sortedAggregateSentences[:self.N]  # tuples here... convert to sentences
		#justTopNSentences = [seq[0] for seq in topNSortedAggregateSentences]
		#justTopNSentences = [seq[0] for seq in sortedAggregateSentences]

		# maximum summary length is measured in words
		summary = ""
		currentWords = 0
		for sentenceTuple in sortedAggregateSentences:
			s = sentenceTuple[0]
			summary += "\n"
			words = s.split()
			currentWords += len(words)
			if currentWords > self.wordCount:
				continue
			summary += " ".join(words)

		return summary.strip()





