__author__ = 'mroylance'

import os
import uuid
import math

nounPhraseKey = "NP"

topicTitleScoreAdjuster = 1

minimalStopWordsFile = "minimalStopWords.txt"
stopWords = {}
if os.path.isfile(minimalStopWordsFile):
	with open(minimalStopWordsFile) as f:
		word = f.readline()
		while word:
			stopWords[word.strip().lower()] = None
			word = f.readline()

class SentenceCluster:
	def __init__(self, sentence, sentenceNumber, topicTitle, headline, mode=1):
		self.sentenceNumber = sentenceNumber
		self.sentence = sentence
		self.simple = sentence.simple
		self.coherencePreviousSentence = sentence.coherencePreviousSentence
		self.coherenceNextSentence = sentence.coherenceNextSentence
		self.coherenceTypes = sentence.coherenceTypes
		self.beginningScore = 0
		self.cleansedTopicTitle = topicTitle.lower().strip()
		self.cleansedHeadline = str(headline).lower().strip()

		if mode == 1:
			self.chunkDict = self.buildChunkDict()
		elif mode == 2:
			self.chunkDict = self.buildBigramChunkDict()
		elif mode == 3:
			self.chunkDict = self.buildChunkDictAll()
		elif mode == 4:
			self.chunkDict = self.buildBigramChunkDictAll()

		self.uniqueId = str(uuid.uuid1())

		if sentenceNumber < 2:
			self.beginningScore += 5

	def buildBigramChunkDict(self):
		chunkDict = {}
		previousChunk = "none"
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			if rootChunk.tag == nounPhraseKey:
				normalizedChunk = str(rootChunk).lower()
				chunkDict[(str(previousChunk), normalizedChunk)] = None
				previousChunk = normalizedChunk
		for chunk in chunkDict:
			if chunk[1] in self.cleansedTopicTitle:
				self.beginningScore += topicTitleScoreAdjuster

			if chunk[1] in self.cleansedHeadline:
				self.beginningScore += topicTitleScoreAdjuster

		return chunkDict

	def buildChunkDict(self):
		chunkDict = {}
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			if rootChunk.tag == nounPhraseKey:
				chunkDict[str(rootChunk).lower().strip()] = None
		for chunk in chunkDict:
			if chunk in self.cleansedTopicTitle:
				self.beginningScore += topicTitleScoreAdjuster

			if chunk in self.cleansedHeadline:
				self.beginningScore += topicTitleScoreAdjuster

		return chunkDict

	def buildChunkDictAll(self):
		chunkDict = {}
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			normalizedChunk = str(rootChunk).lower().strip()

			if normalizedChunk in stopWords:
				continue

			chunkDict[normalizedChunk] = None

		for chunk in chunkDict:
			if chunk in self.cleansedTopicTitle:
				self.beginningScore += topicTitleScoreAdjuster

			if chunk in self.cleansedHeadline:
				self.beginningScore += topicTitleScoreAdjuster

		return chunkDict

	def buildBigramChunkDictAll(self):
		chunkDict = {}
		previousChunk = "none"
		for chunk in self.sentence:
			rootChunk = self.getRootAnaphora(chunk)
			normalizedChunk = str(rootChunk).lower().strip()

			if normalizedChunk in stopWords:
				continue

			chunkDict[(str(previousChunk), normalizedChunk)] = None
			previousChunk = normalizedChunk

		for chunk in chunkDict:
			if chunk[1] in self.cleansedTopicTitle:
				self.beginningScore += topicTitleScoreAdjuster

			if chunk[1] in self.cleansedHeadline:
				self.beginningScore += topicTitleScoreAdjuster

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

