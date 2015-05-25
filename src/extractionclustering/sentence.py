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

		if self.sentenceNum < 2:
			self.beginningScore = 20 - self.sentenceNum

		self.assignEntityScores()
		self.removeArticleHeader()

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

		for keyword in self.keywordResults:
			normalizedWord = keyword[1]
			posTypes = keyword[3]

			for otherKeyword in otherSentence.keywordResults:
				otherNormalizedWord = otherKeyword[1]

				foundMatch = False
				for otherPos in otherKeyword[3]:
					if otherPos in posTypes:
						foundMatch = True
						break

				if otherNormalizedWord == normalizedWord and foundMatch:
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