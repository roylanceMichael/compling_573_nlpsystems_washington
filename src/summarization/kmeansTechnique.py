__author__ = 'mroylance'

from summaryTechnique import SummaryTechnique
import npclustering.kmeans

class KMeansTechnique(SummaryTechnique):
	def rankSentences(self, parameters):
		allPoints = []

		for point in npclustering.kmeans.buildPointForEachSentence(self.docModels):
			allPoints.append(point)

		initialPoints = npclustering.kmeans.getInitialKPoints(allPoints, 3)

		clusters = npclustering.kmeans.performKMeans(initialPoints, allPoints)

		for cluster in clusters:
			self[cluster.highestScoringPoint().sentence.simple] = 1
