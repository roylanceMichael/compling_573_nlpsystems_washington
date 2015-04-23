__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from kmeans.kMeans import KMeans


class KMeansSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		kMeansInstance = KMeans(self.docModels)
		self.addTuplesToDict(kMeansInstance.buildDistances())

	def addTuplesToDict(self, tuples):
		for sentenceTuple in tuples:
			self[sentenceTuple[0].simple] = sentenceTuple[1]
