__author__ = 'mroylance'

from summaryTechnique import SummaryTechnique
from sentenceDistanceSummaryTechnique import SentenceDistanceSummaryTechnique
from sentenceLengthSummaryTechnique import SentenceLengthSummaryTechnique
from npClusteringTechnique import NpClusteringSummaryTechnique
from tfidfSummaryTechnique import TfidfSummaryTechnique
from matrixSummaryTechnique import MatrixSummaryTechnique
from model.doc_model import Cluster
import operator

class InitialSummarizer:
    def __init__(self, docModels, idf, tryTfIdf, tryMatrix, trySentenceDistance, trySentenceLength, tryNpClustering):
        self.docModels = docModels
        self.idf = idf
        self.N = 10  # keep the top N sentences for each technique

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

    def getBestSentences(self):
		aggregateSentences = {}
		for model in self.docModels:
			for sentence in model.cleanSentences():
				sum = 0.0
				for technique in self.techniques:
					sum += technique[sentence]
				aggregateSentences[sentence] = sum
		sortedAggregateSentences = sorted(aggregateSentences.items(), key=operator.itemgetter(1), reverse=True)
		topNSortedAggregateSentences = sortedAggregateSentences[:self.N]  # tuples here... convert to sentences
		justTopNSentences = [seq[0] for seq in topNSortedAggregateSentences]
		return '\n'.join(justTopNSentences)





