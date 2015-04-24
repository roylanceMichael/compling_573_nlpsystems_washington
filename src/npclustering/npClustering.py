__author__ = 'mroylance'
import paragraphCluster
import sentenceCluster
import collections
import operator


class NpClustering:
	def __init__(self, docModels):
		self.docModels = docModels

	def buildSentenceDistances(self):
		sentences = {}
		for docModel in self.docModels:
			sentenceNumber = 0
			for paragraph in docModel.paragraphs:
				for sentence in paragraph:
					sentenceNumber += 1
					newSentence = sentenceCluster.SentenceCluster(sentence, sentenceNumber)
					sentences[newSentence.uniqueId] = newSentence

		distancePairs = {}
		for sentenceId in sentences:
			sentence = sentences[sentenceId]
			for otherSentenceId in sentences:
				if sentenceId == otherSentenceId:
					continue

				otherSentence = sentences[otherSentenceId]
				tupleDistance = sentence.distance(otherSentence)

				if distancePairs.has_key(sentence.uniqueId):
					distancePairs[sentenceId] += tupleDistance
				else:
					distancePairs[sentenceId] = tupleDistance

		# which distancePairs have the highest score?
		for tupleResult in sorted(distancePairs.items(), key=operator.itemgetter(1), reverse=True):
			sentence = sentences[tupleResult[0]]
			score = tupleResult[1]
			yield (sentence.sentence, score)


	def buildDistances(self):
		paragraphs = {}
		for docModel in self.docModels:
			for paragraph in docModel.paragraphs:
				newParagraph = paragraphCluster.ParagraphCluster(paragraph)
				paragraphs[newParagraph.uniqueId] = newParagraph

		distancePairs = {}
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