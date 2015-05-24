__author__ = 'mroylance'
import uuid
import math

nounPhraseKey = "NP"


class SentenceCluster:
	def __init__(self, sentence, sentenceNumber, topicTitle, headline, useUnigram=True):
		self.sentenceNumber = sentenceNumber
		self.sentence = sentence
		self.simple = sentence.simple
		self.coherencePreviousSentence = sentence.coherencePreviousSentence
		self.coherenceNextSentence = sentence.coherenceNextSentence
		self.coherenceTypes = sentence.coherenceTypes
		self.beginningScore = 0
		self.cleansedTopicTitle = topicTitle.lower().strip()
		self.cleansedHeadline = headline.lower().strip()

		if useUnigram:
			self.chunkDict = self.buildChunkDict()
			for chunk in self.chunkDict:
				if chunk in self.cleansedTopicTitle:
					self.beginningScore += 20

				if chunk in self.cleansedHeadline:
					self.beginningScore += 20
		else:
			self.chunkDict = self.buildBigramChunkDict()
			for chunk in self.chunkDict:
				if chunk[1] in self.cleansedTopicTitle:
					self.beginningScore += 20

				if chunk[1] in self.cleansedHeadline:
					self.beginningScore += 20

		self.uniqueId = str(uuid.uuid1())

		if sentenceNumber < 2:
			self.beginningScore += 20

	def buildBigramChunkDict(self):
		chunkDict = {}
		previousChunk = "none"
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			if rootChunk.tag == nounPhraseKey:
				normalizedChunk = str(rootChunk).lower()
				chunkDict[(str(previousChunk), normalizedChunk)] = None
				previousChunk = normalizedChunk
		return chunkDict

	def buildChunkDict(self):
		chunkDict = {}
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			if rootChunk.tag == nounPhraseKey:
				chunkDict[str(chunk).lower()] = None

		return chunkDict

	def getRootAnaphora(self, chunk):
		if chunk.anaphora is None:
			return chunk
		return self.getRootAnaphora(chunk.anaphora)

	def distance(self, otherSentence):
		sameTotal = self.beginningScore

		for otherChunk in otherSentence.chunkDict:
			if otherChunk in self.chunkDict:
				sameTotal += 1

		# todo: work out better
		# sameTotal -= math.fabs (len(self.chunkDict) - len(otherParagraph.chunkDict))

		return sameTotal

