__author__ = 'mroylance'
import uuid
import math


class ParagraphCluster:
    def __init__(self, paragraph):
        self.paragraph = paragraph
        self.chunkDict = self.buildChunkDict()
        self.uniqueId = str(uuid.uuid1())

    def buildChunkDict(self):
        chunkDict = {}
        for sentence in self.paragraph:
            for chunk in sentence:
                chunkDict[str(chunk).lower()] = None
        return chunkDict

    def distance(self, otherParagraph):
        sameTotal = 0

        for otherChunk in otherParagraph.chunkDict:
            if otherChunk in self.chunkDict:
                sameTotal += 1

        # todo: work out better
        # sameTotal -= math.fabs (len(self.chunkDict) - len(otherParagraph.chunkDict))

        return sameTotal

