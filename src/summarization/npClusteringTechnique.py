__author__ = 'thomas'

from summaryTechnique import SummaryTechnique
from npclustering.npClustering import NpClustering


class NpClusteringSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		self.docModels.processNPs()
		instance = NpClustering(self.docModels)

		for sentenceTuple in instance.buildSentenceDistances():
			self[sentenceTuple[0].simple] = sentenceTuple[1]