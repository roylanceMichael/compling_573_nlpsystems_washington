from selection import similarity
import summarization.summaryTechnique
from model.doc_model import Cluster, Sentence


class MatrixSummaryTechnique(summarization.summaryTechnique.SummaryTechnique):
	def rankSentences(self):
		# testSentences = ("Test sentence one.", "This is test sentence two.", "Sentence three.", "Here is the final sentence.")
		#testSentences = tuple(Sentence(s, None, 0) for s in testSentences)
		cluster = Cluster(self.docModels)
		matrix = similarity.DenseGraph(cluster.sentences(), similarity.cosine2b)
		step = 1.0 / matrix._sNum
		rank = 0.0
		for s in matrix.pullinorder():
			self[s.simple] = 1.0 - (step * rank)
			rank += 1.0


if __name__ == '__main__':
	mst = MatrixSummaryTechnique(True, 1.0, None)
	mst.rankSentences()
	print(mst)



