__author__ = 'mroylance'

import uuid


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
			t1 = triple.triple.t1
			t1Value= t1.value.lower()
			t1Sem = t1.sem_tags.lower()

			t2 = triple.triple.t2
			t2Value = t2.value.lower()
			t2Sem = t2.sem_tags.lower()

			t3 = triple.triple.t3
			t3Value = t3.value.lower()
			t3Sem = t3.sem_tags.lower()

			for otherTriple in otherSentence.triples:
				otherT1 = otherTriple.triple.t1
				otherT1Value= otherT1.value.lower()
				otherT1Sem = otherT1.sem_tags.lower()

				otherT2 = otherTriple.triple.t2
				otherT2Value = otherT2.value.lower()
				otherT2Sem = otherT2.sem_tags.lower()

				otherT3 = otherTriple.triple.t3
				otherT3Value = otherT3.value.lower()
				otherT3Sem = otherT3.sem_tags.lower()

				if t1Value == otherT1Value:
					score += 1
				if t1Sem == otherT1Sem:
					score += 1
				if t2Value == otherT2Value:
					score += 1
				if t2Sem == otherT2Sem:
					score += 1
				if t3Value == otherT3Value:
					score += 1
				if t3Sem == otherT3Sem:
					score += 1

		for entity in self.entities:
			ent = entity.entity
			displayText = ent.display_text
			semTags = {}
			for item in ent.sem_tags.split(":"):
				semTags[item] = None
			domainRole = ent.domain_role

			for otherEntity in otherSentence.entities:
				otherEnt = otherEntity.entity
				otherDisplayText = otherEnt.display_text
				otherDomainRole = otherEnt.domain_role

				otherSemTags = {}
				for item in otherEnt.sem_tags.split(":"):
					if item in semTags:
						score += 1

				if displayText == otherDisplayText:
					score += 1

				if domainRole == otherDomainRole:
					score += 1

		return score

