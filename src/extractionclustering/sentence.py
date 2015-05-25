__author__ = 'mroylance'

import uuid

ignoreTriples = {"<empty>": None, "<unspecified>": None}
subjectScore = 3.0
objectScore = 2.0
obliqueScore = 1.0

passiveBe = ["were", "was"]


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
				subStr = self.simple[0:result]
				uppers = [l for l in subStr if l.isupper()]

				if float(len(uppers)) > float(len(subStr) / 2):
					self.simple = self.simple[result+len(beginningArticle):]
					break

		self.simple = self.simple.strip()

	def distanceToOtherSentence(self, otherSentence):
		score = self.beginningScore

		"""
		for phrase in self.phrases:
			root = phrase[2].lower()
			for otherPhrase in otherSentence.phrases:
				otherRoot = otherPhrase[2].lower()
				if root == otherRoot:
					score += 1
		"""
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