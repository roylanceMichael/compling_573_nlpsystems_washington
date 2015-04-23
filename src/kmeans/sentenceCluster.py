__author__ = 'mroylance'
import uuid
import math


class SentenceCluster:
    def __init__(self, sentence):
        self.sentence = sentence
        self.chunkDict = self.buildChunkDict()
        self.uniqueId = uuid.uuid1()

    def buildChunkDict(self):
        chunkDict = {}
        for chunk in self.sentence:
            chunkDict[str(chunk).lower()] = None
        return chunkDict

    def distance(self, otherSentence):
        # x1 * x2 / x1^2 + x2^2
        sameTotal = 0

        for otherChunk in otherSentence.chunkDict:
            if otherChunk not in self.chunkDict: # and feature in self.tr.keptFeatures:
                sameTotal += 1

        sameTotal -= math.fabs(len(self.chunkDict) - len(otherSentence.chunkDict)) / 2

        return sameTotal

