from selection.similarity import UnidirectedGraph, DirectedGraph, cosine2
from summaryTechnique import SummaryTechnique
from model.doc_model import Cluster, Sentence
from collections import Counter


class GraphSummaryTechnique(SummaryTechnique):
    def __init__(self, enabled, weight, docCluster, techniqueName, cosignweight, pullfactor=-1.0, initialwindow=2,
                 initialbonus=4, topicvocab=None, independentweights=Counter()):
        docCluster.processNPs()
        self.docCluster, self.cosignweight, self.pullfactor, self.initialwindow, self.initialbonus, self.topicvocab, self.independentweights\
            = docCluster, cosignweight, pullfactor, initialwindow, initialbonus, topicvocab, independentweights
        self.directed = cosignweight == 1.0 or initialwindow == 0
        SummaryTechnique.__init__(self, enabled, weight, docCluster, techniqueName)


    def NPSimilarity(self, sentencepair):
        return sentencepair[0].distance(sentencepair[1], self.initialwindow, self.initialbonus)


    def rankSentences(self, paramaters):
        if not self.cosignweight:
            distancemetric = self.NPSimilarity
        elif self.cosignweight == 1.0:
            distancemetric = lambda x: cosine2(x, self.topicvocab)
        else:
            npweight = 1-self.cosignweight
            distancemetric = lambda x: self.cosignweight * cosine2(x, self.topicvocab) + npweight * self.NPSimilarity(x)

        if self.directed:
            matrix = DirectedGraph(self.docCluster.sentences(), distancemetric, self.independentweights)
        else:
            matrix = UnidirectedGraph(self.docCluster.sentences(), distancemetric, self.independentweights)
        step = 1.0 / matrix._sNum
        rank = 0.0
        itterator = matrix.simpleorder() if self.pullfactor == 1.0 else matrix.pullinorder(self.pullfactor)
        #for s in matrix.simpleorder():
        for s in itterator:
            self[s.simple] = 1.0 - (step * rank)
            rank += 1.0




