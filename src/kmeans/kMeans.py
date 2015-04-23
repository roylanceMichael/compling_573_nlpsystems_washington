__author__ = 'mroylance'
import paragraphCluster
import collections
import operator


class KMeans:
    def __init__(self, docModels):
        self.docModels = docModels

    def buildDistances(self):
        paragraphs = { }
        for docModel in self.docModels:
            for paragraph in docModel.paragraphs:
                newParagraph = paragraphCluster.ParagraphCluster(paragraph)
                paragraphs[newParagraph.uniqueId] = newParagraph

        distancePairs = { }
        for paragraphId in paragraphs:
            paragraph = paragraphs[paragraphId]
            for otherParagraphId in paragraphs:
                if paragraphId == otherParagraphId:
                    continue

                otherParagraph = paragraphs[otherParagraphId]
                tupleDistance = paragraph.distance(otherParagraph)

                if distancePairs.has_key(paragraph.uniqueId):
                    distancePairs[paragraphId] += tupleDistance
                else:
                    distancePairs[paragraphId] = tupleDistance

        # which distancePairs have the highest score?
        for tupleResult in sorted(distancePairs.items(), key=operator.itemgetter(1), reverse=True):
            paragraph = paragraphs[tupleResult[0]]
            score = tupleResult[1]
            yield (paragraph.paragraph, score)


