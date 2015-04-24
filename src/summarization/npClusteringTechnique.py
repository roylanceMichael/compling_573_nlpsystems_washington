__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from npclustering.npClustering import NpClustering


class NpClusteringSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		instance = NpClustering(self.docModels)
		self.addTuplesToDict(instance.buildSentenceDistances())

	def addTuplesToDict(self, tuples):
		max = 4
		idx = 0
		for sentenceTuple in tuples:
			if idx > max:
				break
			self[sentenceTuple[0].simple] = sentenceTuple[1]
			idx += 1
