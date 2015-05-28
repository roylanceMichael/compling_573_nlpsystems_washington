__author__ = 'mroylance'

import os
import re
import uuid

ignoreTriples = {"<empty>": None, "<unspecified>": None}
subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0

passiveBe = ["were", "was"]

allPosTypes = {u'INFINITIVE_TO': None, u'REC_PRONOUN': None, u'PRES_PART': None, u'INTERJ': None, u'MODAL': None, u'PAST_PART': None, u'POSS_PRONOUN': None, u'CONJ': None, u'NOUN': None, u'DEMONSTRATIVE': None, u'REF_PRONOUN': None, u'ARTICLE': None, u'AUX': None, u'GERUND': None, u'REL_PRONOUN': None, u'COPULAR': None, u'VERB': None, u'PARTICLE': None, u'CLAUSE_MARKER': None, u'QUANTIFIER': None, u'QUESTION_MARKER': None, u'ADVERB': None, u'PRONOUN': None, u'ADJECTIVE': None, u'PREP': None}

minimalStopWordsFile = "minimalStopWords.txt"
stopWords = {}
if os.path.isfile(minimalStopWordsFile):
	with open(minimalStopWordsFile) as f:
		word = f.readline()
		while word:
			stopWords[word.strip().lower()] = None
			word = f.readline()

class Sentence:
	def __init__(self, text, id, sentenceNum, docModel, topicTitleDict, goldSentences=None, keywordTopicMatchScore=5):
		# self.simple = re.sub("[^a-zA-Z0-9 -]", "",  re.sub("\s+", " ", text))
		self.simple = re.sub("\s+", " ", text)
		self.uuid = str(uuid.uuid1())
		self.id = id
		self.sentenceNum = sentenceNum
		self.docModel = docModel
		self.triples = []
		self.entities = []
		self.entityScores = {}
		self.facts = []
		self.phrases = []
		self.keywordResults = []
		self.factRelations = []
		self.beginningScore = 0
		self.nounChunks = []
		self.topicTitleDict = topicTitleDict
		self.chunkDictLen = 0
		self.goldSentences = goldSentences

		self.keywordTopicMatchScore = keywordTopicMatchScore

		self.chunkDict = {}

		if self.sentenceNum < 2:
			self.beginningScore = 5 - self.sentenceNum

		self.assignEntityScores()
		self.removeArticleHeader()

	def __str__(self):
		return self.uuid + " " + self.simple

	def applyGoldSentencePreferences(self):
		if self.goldSentences is not None:
			for sentenceId in self.goldSentences:
				otherSentence = self.goldSentences[sentenceId]
				self.beginningScore += self.distanceToOtherSentence(otherSentence)

	def createChunks(self, chunkMethod):
		if chunkMethod == 1:
			for keywordResult in self.keywordResults:
				normalizedKeyword = keywordResult[1].strip().lower()

				if normalizedKeyword in self.topicTitleDict:
					self.beginningScore += self.keywordTopicMatchScore

				if len(normalizedKeyword) == 0 or normalizedKeyword in stopWords:
					continue
				self.chunkDict[normalizedKeyword] = None
		elif chunkMethod == 2:
			previousKeyword = None
			for keywordResult in self.keywordResults:
				normalizedKeyword = keywordResult[1].strip().lower()

				if normalizedKeyword in self.topicTitleDict:
					self.beginningScore += self.keywordTopicMatchScore

				if len(normalizedKeyword) == 0 or normalizedKeyword in stopWords:
					continue
				if previousKeyword is None:
					previousKeyword = normalizedKeyword
					continue

				self.chunkDict[(previousKeyword, normalizedKeyword)] = None
				previousKeyword = normalizedKeyword
		elif chunkMethod == 3:
			previousKeyword = None
			previousPreviousKeyword = None
			for keywordResult in self.keywordResults:
				normalizedKeyword = keywordResult[1].strip().lower()

				if normalizedKeyword in self.topicTitleDict:
					self.beginningScore += self.keywordTopicMatchScore

				if len(normalizedKeyword) == 0 or normalizedKeyword in stopWords:
					continue

				if previousKeyword is None or previousPreviousKeyword is None:
					previousPreviousKeyword = previousKeyword
					previousKeyword = normalizedKeyword
					continue

				self.chunkDict[(previousPreviousKeyword, previousKeyword, normalizedKeyword)] = None
				previousPreviousKeyword = previousKeyword
				previousKeyword = normalizedKeyword
		elif chunkMethod == 4:
			for chunk in self.nounChunks:
				self.chunkDict[chunk] = None
		elif chunkMethod == 5:
			previousChunk = None
			for chunk in self.nounChunks:
				if previousChunk is None:
					previousChunk = chunk
					continue

				self.chunkDict[(previousChunk, chunk)] = None
				previousChunk = chunk

		self.chunkDictLen = float(len(self.chunkDict))

	def determineNounChunks(self):
		nounChunk = []
		for keyword in self.keywordResults:
			foundNounyThing = False

			for pos in keyword[3]:
				if pos == 'NOUN' or pos == 'ADJECTIVE' and len(keyword[1].strip()) > 0:
					normalizedKeyword = keyword[1].lower().strip()

					if normalizedKeyword in self.topicTitleDict:
						self.beginningScore += self.keywordTopicMatchScore

					nounChunk.append(normalizedKeyword)
					foundNounyThing = True
					break

			if foundNounyThing == False and len(nounChunk) > 0:
				self.nounChunks.append(tuple(nounChunk))
				nounChunk = []

	def assignEntityScores(self):
		# 40 40 20 split
		totalEntities = len(self.entities)
		firstForty = float(totalEntities*.4)
		secondForty = float(firstForty + (totalEntities * 0.4))

		isPassive = False
		for keyword in self.keywordResults:
			if keyword[1] == "be" and keyword[2] in passiveBe:
				isPassive = True

		idx = 0
		for entity in self.entities:
			if idx <= firstForty:
				if isPassive:
					self.entityScores[entity] = objectScore
				else:
					self.entityScores[entity] = subjectScore
			elif idx <= secondForty:
				if isPassive:
					self.entityScores[entity] = subjectScore
				else:
					self.entityScores[entity] = objectScore
			else:
				self.entityScores[entity] = obliqueScore
			idx += 1

	def removeArticleHeader(self):
		beginningArticles = ["--", "_"]
		allCapsOrNotLowerAlpha = "[[:upper:]0-9-]{5,}"

		# for beginningArticle in beginningArticles:
		# 	result = self.simple.find(beginningArticle, 0)
		#
		# 	if result > -1:
		# 		self.simple = self.simple[result+len(beginningArticle):]

		allCapsOrNotLowerAlphaResult = self.simple.find(allCapsOrNotLowerAlpha, 0)
		if allCapsOrNotLowerAlphaResult > -1:
			self.simple = self.simple[allCapsOrNotLowerAlphaResult:]

		self.simple = self.simple.strip()

	def distanceToOtherSentence(self, otherSentence):
		score = self.beginningScore

		# for otherChunk in otherSentence.chunkDict:
		# 	if otherChunk in self.chunkDict:
		# 		score += 1

		# smoothing
		return score
		# return score / (self.chunkDictLen + otherSentence.chunkDictLen + 1)

		"""
		for phrase in self.phrases:
			root = phrase[2].lower()
			for otherPhrase in otherSentence.phrases:
				otherRoot = otherPhrase[2].lower()
				if root == otherRoot:
					score += 1

		for fact in self.facts:
			element = fact[1].lower()
			mode = fact[2].lower()
			for otherFact in otherSentence.facts:
				otherElement = otherFact[1].lower()
				otherMode = otherFact[2].lower()

				if mode == otherMode and element == otherElement:
					score += 1

		for triple in self.triples:
			t1Value= triple[1].lower()
			t1Sem = triple[2].lower()
			t2Value = triple[3].lower()
			t2Sem = triple[4].lower()

			t3Value = triple[5].lower()
			t3Sem = triple[6].lower()

			for otherTriple in otherSentence.triples:
				otherT1Value= otherTriple[1].lower()
				otherT1Sem = otherTriple[2].lower()

				otherT2Value = otherTriple[3].lower()
				otherT2Sem = otherTriple[4].lower()

				otherT3Value = otherTriple[5].lower()
				otherT3Sem = otherTriple[6].lower()

				if (t1Value == otherT1Value and
							t3Value == otherT3Value and
							(t1Value not in ignoreTriples and
							t3Value not in ignoreTriples)):
					score += 1

		for entity in self.entities:
			displayText = entity[1].lower()
			domainRole = entity[3].lower()

			for otherEntity in otherSentence.entities:
				otherDisplayText = otherEntity[1].lower()
				otherDomainRole = otherEntity[3].lower()

				if domainRole == otherDomainRole and displayText == otherDisplayText:
					score += 1

		return score
		"""


def hasVerb(sentence):
	for keyword in sentence.keywordResults:
		if sentence.simple == "one for each victim.":
			pass
		for POS in keyword[3]:
			if POS == "VERB" or POS == "PAST_PART" or POS == "PRES_PART" or POS == "AUX" or POS == "MODAL" or POS == "GERUND":
				return True
	return False


def factory(topicDictionary, topicTitleDict, goldSentences=None):
	allSentences = {}

	for docNo in topicDictionary:

		docModel = topicDictionary[docNo]
		for paragraph in docModel.paragraphs:
			sentences = {}
			sentenceNum = 0
			for sentence in paragraph.extractionSentences:
				text = paragraph.text
				actualSentence = text[sentence[1]:sentence[1] + sentence[2]]
				sentences[sentence[0]] = \
					Sentence(
						actualSentence,
						sentence[0],
						sentenceNum,
						docModel,
						topicTitleDict,
						goldSentences)
				sentenceNum += 1

			for keywordResult in paragraph.extractionKeywordResults:
				if keywordResult[0] in sentences:
					sentences[keywordResult[0]].keywordResults.append(keywordResult)

			for triple in paragraph.extractionTriples:
				sentences[triple[0]].triples.append(triple)

			for entity in paragraph.extractionEntities:
				sentences[entity[0]].entities.append(entity)

			for fact in paragraph.extractionFacts:
				sentences[fact[0]].facts.append(fact)

			for phrase in paragraph.extractionTextPhrases:
				sentences[phrase[0]].phrases.append(phrase)

			for sentence in sentences:
				sentences[sentence].assignEntityScores()
				sentences[sentence].determineNounChunks()
				sentences[sentence].createChunks(4)
				# toggle on and off...
				sentences[sentence].applyGoldSentencePreferences()

				if len(sentences[sentence].triples) != 0 \
					and not "''" in sentences[sentence].simple \
					and not "``" in sentences[sentence].simple \
					and hasVerb(sentences[sentence]):

					allSentences[sentences[sentence].uuid] = sentences[sentence]

	return allSentences
