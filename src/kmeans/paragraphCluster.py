__author__ = 'mroylance'
import uuid
import math


class ParagraphCluster:
    def __init__(self, paragraph):
        self.paragraph = paragraph
        self.chunkDict = self.buildChunkDict()
        self.uniqueId = uuid.uuid1()

    def buildChunkDict(self):
        chunkDict = {}
        for sentence in self.paragraph:
            for chunk in sentence:
                chunkDict[str(chunk).lower()] = None
        return chunkDict

    def distance(self, otherParagraph):
        # x1 * x2 / x1^2 + x2^2
        sameTotal = 0

        for otherChunk in otherParagraph.chunkDict:
            if otherChunk not in self.chunkDict: # and feature in self.tr.keptFeatures:
                sameTotal += 1

        sameTotal -= math.fabs(len(self.chunkDict) - len(otherParagraph.chunkDict)) / 2

        return sameTotal

