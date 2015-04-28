from selection.similarity import DenseGraph, cosine2b
from summaryTechnique import SummaryTechnique
from model.doc_model import Cluster, Sentence


class MatrixSummaryTechnique(SummaryTechnique):
    def __init__(self, enabled, weight, docCluster, techniqueName):
        self.docCluster = docCluster
        SummaryTechnique.__init__(self, enabled, weight, docCluster, techniqueName)


    def rankSentences(self):
        #testSentences = ("Test sentence one.", "This is test sentence two.", "Sentence three.", "Here is the final sentence.")
        #testSentences = tuple(Sentence(s, None, 0) for s in testSentences)
        matrix = DenseGraph(self.docCluster.sentences(), cosine2b)
        step = 1.0 / matrix._sNum
        rank = 0.0
        for s in matrix.pullinorder():
            self[s.simple] = 1.0 - (step * rank)
            rank += 1.0




