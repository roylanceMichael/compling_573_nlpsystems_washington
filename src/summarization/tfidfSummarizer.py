import model.idf
from model.doc_model import Cluster
from summaryTechnique import SummaryTechnique
"""
class matrixSummaryTechnique(SummaryTechnique):
    def rankSentences(self):

        cluster = Cluster(self.docModels)
        sentences = [cluster.sentences()]
        scores = list()
        for s in sentences:
            for w in s.words():
                word = w.full.lower()
                if word in
"""