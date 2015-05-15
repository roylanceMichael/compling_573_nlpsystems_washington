from selection.similarity import cosine2
from summaryTechnique import SummaryTechnique
from model.doc_model import Cluster, Sentence


class TopicSimSummaryTechnique(SummaryTechnique):
    def __init__(self, enabled, weight, docCluster, techniqueName):
        self.docCluster = docCluster
        SummaryTechnique.__init__(self, enabled, weight, docCluster, techniqueName)


    def rankSentences(self):
        topic = self.docCluster.topic
        sentences = list(self.docCluster.sentences())
        scores = list(cosine2((x, topic)) for x in sentences)
        maxscore = max(scores)
        for i in range(len(sentences)):
            self[sentences[i].simple] = scores[i] / maxscore
