__author__ = 'mroylance'

import types

pronounType = "PRP"
verbBaseType = "VB"
thenWord = "then"
alsoWord = "also"


# todo: update with the different types
def isPronounSubject(sentence):
	foundPronoun = False
	for chunk in sentence:
		if chunk.tag in pronounType:
			foundPronoun = True

		if verbBaseType in chunk.tag:
			return foundPronoun

	return foundPronoun


def isThenInSubject(sentence):
	for chunk in sentence:
		if str(chunk).lower() == thenWord:
			return True

		if verbBaseType in chunk.tag:
			return False

	return False


def isAlsoInSubject(sentence):
	for chunk in sentence:
		if str(chunk).lower() == alsoWord:
			return True
	return False


def determineDoc(docModel):
	for paragraph in docModel.paragraphs:
		determine(paragraph)


def determine(paragraph):
	# we're looking for pronouns here
	sentenceTuples = []
	previousSentence = None
	for sentence in paragraph:
		if previousSentence != None:
			sentenceTuples.append((previousSentence, sentence))
		previousSentence = sentence

	for (firstSentence, secondSentence) in sentenceTuples:
		if not isPronounSubject(firstSentence):
			firstSentence.coherenceTypes.append(types.occasion)
			secondSentence.coherenceTypes.append(types.occasion)
			secondSentence.coherenceTypes.append(types.explanation)

			hookUpBothSentences(firstSentence, secondSentence)
		else:
			secondSentence.coherenceTypes.append(types.explanation)

			hookUpBothSentences(firstSentence, secondSentence)

		if not isAlsoInSubject(firstSentence) and isAlsoInSubject(secondSentence):
			firstSentence.coherenceTypes.append(types.parallel)
			secondSentence.coherenceTypes.append(types.parallel)

			hookUpBothSentences(firstSentence, secondSentence)


def hookUpBothSentences(firstSentence, secondSentence):
	firstSentence.coherenceNextSentence = secondSentence
	secondSentence.coherencePreviousSentence = firstSentence