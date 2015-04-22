from collections import defaultdict

from nltk.corpus import stopwords
import string

from model.doc_model import Sentence
from model.idf import stopWords

def cosine2(sentencePair, vocab=None):
    counts = defaultdict(lambda: [0,0])

    for i in (0, 1):
        for w in sentencePair[i].words():
            word = w.full.lower()
            if vocab and word not in vocab:
                continue
            elif word in stopWords:
                continue

            counts[word][i] += 1

    magnitudes = [0.0, 0.0]
    dotProd = 0.0
    for value in counts.values():
        for i in (0,1):
            magnitudes[i] += value[i]**2
        dotProd += value[0]*value[1]

    # can't do cosine similarity of one of the sentences has no in-vocab words
    # return 0 (completely dissimilar) in this case
    for i in (0,1):
        if magnitudes[i] == 0.0:
            return 0

    return dotProd**2 / (magnitudes[0] * magnitudes[1])

class DenseGraph(list):
    def __init__(self, sentences, simMeasure):
        self.sentences = sentences if isinstance(sentences, list) else list(sentences)
        self._sNum = len(self.sentences)
        list.__init__(self)
        for x in range(self._sNum):
            row = list()
            for y in range(x):
                row.append( simMeasure((self.sentences[x], self.sentences[y])) )
            row.append(1.0)
            self.append(row)

    def __str__(self):
        return list.__str__(self)

    def getSim(self, sID0, sID1):
        if sID0 > sID1:
            return self[sID0][sID1]
        return self[sID1][sID0]

    def setSim(self, sID0, sID1, value):
        if sID0 > sID1:
            self[sID0][sID1] = value
        else:
            [sID1][sID0] = value

    def makeNeg(self, sID0, sID1):
        #print(( sID0, sID1))
        #print(sID0 > sID1)
        if sID0 > sID1:
            if self[sID0][sID1] > 0:
                self[sID0][sID1] *= -1
        elif self[sID1][sID0] > 0:
            self[sID1][sID0] *= -1

    # returns the sentence most similar to everything else,
    # then turns its sim scores with everything negative
    def pullMax(self):
        id = max(
            (
                sum( self.getSim(x, y) for y in range(self._sNum) ),
                x
            ) for x in range(self._sNum)
        )[1]

        for y in range(self._sNum):
            self.makeNeg(id, y)

        return id

if __name__ == '__main__':
    testSentences = ("Test sentence one.", "This is test sentence two.", "Sentence three.", "Here is the final sentence.")
    testSentences = tuple(Sentence(s, None, 0) for s in testSentences)
    simMeasure = lambda s: cosine2(s)
    graph = DenseGraph(testSentences, simMeasure)
    print(graph)
    print(graph.getSim(0,2))
    print(graph.getSim(2,0))
    print(graph.pullMax())
    print(graph.pullMax())