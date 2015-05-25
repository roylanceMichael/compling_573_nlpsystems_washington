__author__ = 'mroylance'

import uuid

ignoreTriples = {"<empty>": None, "<unspecified>": None}
subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0

passiveBe = ["were", "was"]

allPosTypes = {u'INFINITIVE_TO': None, u'REC_PRONOUN': None, u'PRES_PART': None, u'INTERJ': None, u'MODAL': None, u'PAST_PART': None, u'POSS_PRONOUN': None, u'CONJ': None, u'NOUN': None, u'DEMONSTRATIVE': None, u'REF_PRONOUN': None, u'ARTICLE': None, u'AUX': None, u'GERUND': None, u'REL_PRONOUN': None, u'COPULAR': None, u'VERB': None, u'PARTICLE': None, u'CLAUSE_MARKER': None, u'QUANTIFIER': None, u'QUESTION_MARKER': None, u'ADVERB': None, u'PRONOUN': None, u'ADJECTIVE': None, u'PREP': None}

class Sentence:
	def __init__(self, text, id, sentenceNum, docModel):
		self.simple = text.strip()
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
		self.uniqueId = str(uuid.uuid1())
		self.nounChunks = []

		self.chunkDict = {}

		if self.sentenceNum < 2:
			self.beginningScore = 5 - self.sentenceNum

		self.assignEntityScores()
		self.removeArticleHeader()

		for chunk in self.nounChunks:
			print chunk

	def createChunks(self, chunkMethod):
		if chunkMethod == 1:
			for keywordResult in self.keywordResults:
				if len(keywordResult[1].strip()) == 0:
					continue
				self.chunkDict[keywordResult[1]] = None
		elif chunkMethod == 2:
			previousKeyword = None
			for keywordResult in self.keywordResults:
				if len(keywordResult[1].strip()) == 0:
					continue
				if previousKeyword is None:
					previousKeyword = keywordResult[1]
					continue

				self.chunkDict[(previousKeyword, keywordResult[1])] = None
				previousKeyword = keywordResult[1]
		elif chunkMethod == 3:
			previousKeyword = None
			previousPreviousKeyword = None
			for keywordResult in self.keywordResults:
				if len(keywordResult[1].strip()) == 0:
					continue

				if previousKeyword is None or previousPreviousKeyword is None:
					previousPreviousKeyword = previousKeyword
					previousKeyword = keywordResult[1]
					continue

				self.chunkDict[(previousPreviousKeyword, previousKeyword, keywordResult[1])] = None
				previousPreviousKeyword = previousKeyword
				previousKeyword = keywordResult[1]
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

	def determineNounChunks(self):
		nounChunk = []
		for keyword in self.keywordResults:
			foundNounyThing = False

			for pos in keyword[3]:
				if pos == 'NOUN' or pos == 'ADJECTIVE' and len(keyword[1].strip()) > 0:
					nounChunk.append(keyword[1])
					foundNounyThing = True

			if foundNounyThing == False and len(nounChunk) > 0:
				self.nounChunks.append(nounChunk)
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

		for beginningArticle in beginningArticles:
			result = self.simple.find(beginningArticle, 0)

			if result > -1:
				self.simple = self.simple[result+len(beginningArticle):]

		self.simple = self.simple.strip()

	def distanceToOtherSentence(self, otherSentence):
		score = self.beginningScore

		for otherChunk in otherSentence.chunkDict:
			if otherChunk in self.chunkDict:
				score += 1

		return score

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