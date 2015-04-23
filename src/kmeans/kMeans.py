__author__ = 'mroylance'
import paragraphCluster
import collections
import operator


class KMeans:
    def __init__(self, docModels):
        self.docModels = docModels

    def buildDistances(self):
        paragraphs = {}
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
                distancePairs[paragraph.uniqueId] += tupleDistance
            else:
                distancePairs[paragraph.uniqueId] = tupleDistance

        # which distancePairs have the highest score?
        od = collections.OrderedDict(sorted(distancePairs.items(), key=operator.itemgetter(1), reverse=True))

        for item in od:
            yield (paragraphs[item].paragraph, od[item])


