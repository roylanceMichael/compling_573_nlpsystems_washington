__author__ = 'mroylance'
import sentenceCluster
import collections
import operator


class KMeans:
    def __init__(self, docModel):
        self.docModel = docModel
        self.featureDict = self.buildFeatureSet()

    def buildFeatureSet(self):
        featureDict = {}
        for paragraph in self.docModel.paragraphs:
            for sentence in paragraph:
                for chunk in sentence:
                    # instantiate a feature dictionary
                    featureDict[str(chunk).lower()] = None

        return featureDict

    def buildDistances(self):
        sentences = {}
        for sentence in self.docModel.paragraphs:
            newSentence = sentenceCluster.SentenceCluster(sentence)
            sentences[newSentence.uniqueId] = newSentence

        distancePairs = { }
        for sentenceId in sentences:
            sentence = sentences[sentenceId]
            for otherSentenceId in sentences:
                if sentenceId == otherSentenceId:
                    continue

            otherSentence = sentences[otherSentenceId]
            tupleDistance = sentence.distance(otherSentence)

            if distancePairs.has_key(sentence.uniqueId):
                distancePairs[sentence.uniqueId] += tupleDistance
            else:
                distancePairs[sentence.uniqueId] = tupleDistance

        # which distancePairs have the highest score?
        od = collections.OrderedDict(sorted(distancePairs.items(), key=operator.itemgetter(1), reverse=True))

        # let's return 4
        for item in od:
            yield (sentences[item].sentence, od[item])


