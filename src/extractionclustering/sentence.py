__author__ = 'mroylance'

import uuid

ignoreTriples = {"<empty>": None, "<unspecified>": None}


class Sentence:
	def __init__(self, text, id, sentenceNum, docModel, paragraph):
		self.simple = text
		self.id = id
		self.sentenceNum = sentenceNum
		self.docModel = docModel
		self.paragraph = paragraph
		self.triples = []
		self.entities = []
		self.beginningScore = 0
		self.uniqueId = str(uuid.uuid1())

		if self.sentenceNum < 2:
			self.beginningScore = 4 - self.sentenceNum

	def distanceToOtherSentence(self, otherSentence):
		score = self.beginningScore

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

				if (t1Value == otherT1Value or
							t3Value == otherT3Value and
							(t1Value not in ignoreTriples and
							t3Value not in ignoreTriples)):

					# print "-----"
					# print t1Value + " " + t2Value + " " + t3Value
					# print otherT1Value + " " + otherT2Value + " " + otherT3Value
					# print "-----"
					score += 100

		for entity in self.entities:
			displayText = entity[1].lower()
			semTags = {}
			for item in entity[2].split(":"):
				semTags[item.lower()] = None
			domainRole = entity[3].lower()

			for otherEntity in otherSentence.entities:
				otherDisplayText = otherEntity[1].lower()
				otherDomainRole = otherEntity[2].lower()

				"""
				otherSemTags = {}
				for item in otherEntity[3].split(":"):
					if item.lower() in semTags:
						score += 1
				"""

				if displayText == otherDisplayText:
					# print displayText + " " + otherDisplayText
					score += 1

				"""
				if domainRole == otherDomainRole:
					score += 1
				"""

		return score

