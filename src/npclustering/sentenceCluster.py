__author__ = 'mroylance'
import uuid
import math

nounPhraseKey = "NP"


class SentenceCluster:
	def __init__(self, sentence, sentenceNumber):
		self.sentenceNumber = sentenceNumber
		self.sentence = sentence
		self.simple = sentence.simple
		self.coherencePreviousSentence = sentence.coherencePreviousSentence
		self.coherenceNextSentence = sentence.coherenceNextSentence
		self.coherenceTypes = sentence.coherenceTypes
		self.chunkDict = self.buildChunkDict()
		self.uniqueId = str(uuid.uuid1())

	def buildChunkDict(self):
		chunkDict = {}
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			if rootChunk.tag == nounPhraseKey:
				chunkDict[str(chunk).lower()] = None

		return chunkDict

	def getRootAnaphora(self, chunk):
		if chunk.anaphora == None:
			return chunk
		return self.getRootAnaphora(chunk.anaphora)

	def distance(self, otherSentence):
		sameTotal = 0

		# give preference to beginning sentences
		if self.sentenceNumber < 2:
			sameTotal += 4 - self.sentenceNumber

		for otherChunk in otherSentence.chunkDict:
			if otherChunk in self.chunkDict:
				sameTotal += 1

		# todo: work out better
		# sameTotal -= math.fabs (len(self.chunkDict) - len(otherParagraph.chunkDict))

		return sameTotal

