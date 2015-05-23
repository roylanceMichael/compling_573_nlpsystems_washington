__author__ = 'mroylance'

from summaryTechnique import SummaryTechnique
from sentenceDistanceSummaryTechnique import SentenceDistanceSummaryTechnique
from sentenceLengthSummaryTechnique import SentenceLengthSummaryTechnique
from topicSimSummaryTechnique import TopicSimSummaryTechnique
from tfidfSummaryTechnique import TfidfSummaryTechnique
from graphSummaryTechnique import GraphSummaryTechnique
from model.doc_model import Cluster
from highestFrequencyTechnique import HighestFrequencyTechnique
from graphSummaryTechnique import GraphSummaryTechnique

import operator

#
# container class for holding summarizers.  These summarizers are descendants
# of the SummaryTechnique abstract base class.
# every SummaryTechnique is weighted and can contribute to the overall score
#
# each summary happens only once, ranking all, then the gets on the summary
# techniques combine the gets with a weight and return a score for each sentence.
#
# from that, we can add up weighted votes for each sentence and select the best one.
#
class InitialSummarizer:
	def __init__(self, docCluster, idf, tryTfIdf, trySentenceDistance, trySentenceLength, tryTopicSim, tryHighestFrequency):
		self.docCluster = docCluster
		self.idf = idf
		self.N = 10  # keep the top N sentences for each technique
		self.wordCount = 100

		self.techniques = list()
		self.tfIdf = TfidfSummaryTechnique(tryTfIdf, 1.0, self.docCluster, "tf-idf")
		self.techniques.append(self.tfIdf)
		self.sentenceDistance = SentenceDistanceSummaryTechnique(trySentenceDistance, 1.0, docCluster, "sdist")
		self.techniques.append(self.sentenceDistance)
		self.sentenceLength = SentenceLengthSummaryTechnique(trySentenceLength, 1.0, docCluster, "slen")
		self.techniques.append(self.sentenceLength)
		self.topicSim = TopicSimSummaryTechnique(tryTopicSim, 1.0, docCluster, "topic")
		self.techniques.append(self.sentenceLength)
		self.highestFrequency = HighestFrequencyTechnique(tryHighestFrequency, 1.0, docCluster, "highest")
		self.techniques.append(self.highestFrequency)
		self.summarize(None)

	def summarize(self, parameters):
		for technique in self.techniques:
			if technique.enabled:
				technique.rankSentences(parameters)
	
	def getBestSentences(self, w_tfidf=None, w_sd=None, w_sl=None, w_topic=None, w_cosign=0.0, w_np=0.0,
		pullfactor=-1.0, initialwindow=2, initialbonus=4, topicsize=75, parameters=None):
		
		# actualSentences = ""
		# for sentence in self.highestFrequency:
		# 	actualSentences = sentence + " " 
		# return actualSentences

		if w_tfidf is not None:
			self.tfIdf.weight = w_tfidf
		if w_sd is not None:
			self.sentenceDistance.weight = w_sd
		if w_sl is not None:
			self.sentenceLength.weight = w_sl
		if w_topic is not None:
			self.topicSim.weight = w_topic
		# self.highestFrequency.weight = 1.0

		aggregateSentences = {}
		for model in self.docCluster:
			for sentence in model.cleanSentences():
				sum = 0.0
				for technique in self.techniques:
					res = technique[sentence]
					sum += res
				aggregateSentences[sentence] = sum

		# feed aggregate scores to graph so it can handle overlap
		graphweight = 2.0 if not w_cosign else w_cosign + w_np
		cosignweight = 0.5 if not w_cosign else w_cosign / (w_cosign + w_np)
		topicvocab = self.docCluster.gettopicvocab(topicsize) if topicsize else None
		self.graph = GraphSummaryTechnique(True, graphweight, self.docCluster, "cosign+np", cosignweight, pullfactor,
			initialwindow, initialbonus, topicvocab, independentweights=aggregateSentences)
		self.graph.rankSentences(parameters)

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





