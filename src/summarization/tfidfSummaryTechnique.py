from model.idf import stopWords
from summaryTechnique import SummaryTechnique
from model.doc_model import Cluster, Sentence


class TfidfSummaryTechnique(SummaryTechnique):
    def __init__(self, enabled, weight, docCluster):
        self.docCluster = docCluster
        SummaryTechnique.__init__(self, enabled, weight, docCluster)


    def rankSentences(self):
        scores = list()
        sentences = list(self.docCluster.sentences())
        for sentence in sentences:
            current = 0.0
            wordforms = list(w.lower for w in sentence.words())
            for word in wordforms:
                if word not in stopWords:
                    current += self.docCluster.getTFIDF(word)
            scores.append(current / len(wordforms))

        maxscore = max(scores)
        for i in range(len(sentences)):
            self[sentences[i].simple] = scores[i] / maxscore
