from selection.similarity import UnidirectedGraph, DirectedGraph, cosine2b
from summaryTechnique import SummaryTechnique
from model.doc_model import Cluster, Sentence

def NPSimilarity(sentencepair):
    return sentencepair[0].distance(sentencepair[1])

class MatrixSummaryTechnique(SummaryTechnique):
    def __init__(self, enabled, weight, docCluster, techniqueName, directed=False, usenp=False, pullfactor=-1.0):
        docCluster.processNPs()
        self.docCluster, self.directed, self.usenp, self.pullfactor = docCluster, directed, usenp, pullfactor
        SummaryTechnique.__init__(self, enabled, weight, docCluster, techniqueName)


    def rankSentences(self):
        distancemetric = NPSimilarity if self.usenp else cosine2b
        if self.directed:
            matrix = DirectedGraph(self.docCluster.sentences(), distancemetric)
        else:
            matrix = UnidirectedGraph(self.docCluster.sentences(), distancemetric)
        step = 1.0 / matrix._sNum
        rank = 0.0
        for s in matrix.simpleorder():
        #for s in matrix.pullinorder(self.pullfactor):
            self[s.simple] = 1.0 - (step * rank)
            rank += 1.0




