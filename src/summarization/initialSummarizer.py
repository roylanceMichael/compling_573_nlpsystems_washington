__author__ = 'mroylance'
import kmeans.kMeans

class InitialSummarizer:
    def __init__(self, docModels, tryTfIdf, tryMatrix, trySentenceDistance, trySentenceLength, tryNpClustering):
        self.docModels = docModels

    def getBestSentences(self):
        kMeansInstance = kmeans.kMeans.KMeans(self.docModels)

        number = 0
        total = 5
        for topItem in kMeansInstance.buildDistances():
            if number > total:
                break
            yield topItem
            number += 1


