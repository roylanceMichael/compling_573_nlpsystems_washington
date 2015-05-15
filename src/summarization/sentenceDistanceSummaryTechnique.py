__author__ = 'thomas'

from summaryTechnique import SummaryTechnique


class SentenceDistanceSummaryTechnique(SummaryTechnique):
	def rankSentences(self):
		# get distance from first sentence
		for model in self.docModels:
			d = 0
			sentences = model.cleanSentences()
			n = float(len(sentences) - 1)
			for sentence in sentences:
				if n == 0:
					self[sentence] = 1.0
				else:
					self[sentence] = (n - d) / n
				d += 1
