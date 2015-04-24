__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from npclustering.npClustering import NpClustering


class NpClusteringSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		instance = NpClustering(self.docModels)
		self.addTuplesToDict(instance.buildSentenceDistances())

	def addTuplesToDict(self, tuples):
		for sentenceTuple in tuples:
			self[sentenceTuple[0].simple] = sentenceTuple[1]
