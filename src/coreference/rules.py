__author__ = 'mroylance'
import collections
import npModel
import editDistance

nounPhraseKey = "NP"
i = "i"
me = "me"
it = "it"

pronounTypes = {"PRP": None, "PRP$": None, "WP": None, "WP$": None}
badWords = ["a", "an", "the", "of"]
badWordsForWordMatching = ["a", "an", "the", "of", "these", "mr", "mr.", "mrs", "mrs."]

# this will determine if the np's match in number
# give higher weight to npModel2 being a pronoun
# generic rules
def articleRule(npModel):
	return 0


def appositiveRule(npModel, sentIdx, sentences):
	return 0


def wordMatchingRule(npModel1, npModel2):
	# do we have an exact match?

	if editDistance.perform(npModel1.normalizedPhrase, npModel2.normalizedPhrase) < 2:
		return -999
	else:
		for splitWord in npModel1.splitWords:
			if splitWord in badWordsForWordMatching:
				continue
			for otherSplitWord in npModel2.splitWords:
				if otherSplitWord in badWordsForWordMatching:
					continue

				if editDistance.perform(splitWord, otherSplitWord) < 2:
					return -10
	return 0


# comparison rules
def matchPlurality(npModel1, npModel2):
	if npModel1.plurality and npModel2.plurality and npModel2.pronounType != npModel.nonePronounType:
		return -999
	if npModel1.plurality and npModel2.plurality:
		return -999
	return 0


def matchGender(npModel1, npModel2):
	if npModel1.gender != npModel.unknown and npModel2.gender != npModel.unknown:
		if npModel1.gender != npModel2.gender:
			return 999
		else:
			return 0
	return 0


# 1 Incompatibility function: 1 if both are proper names, but mismatch on every word; else 0
def properNamesRule(npModel1, npModel2):
	if npModel1.properName and npModel2.properName:
		for firstWord in npModel1.splitWords:
			for secondWord in npModel2.splitWords:
				if firstWord == secondWord:
					return 0
		return 999
	return 0


def pronounTypesRule(npModel1, npModel2):
	if npModel1.pronounType != npModel.nonePronounType and npModel2.pronounType != npModel.nonePronounType:
		return 0
	return 1


def mismatchWordsRule(npModel1, npModel2):
	firstWords = npModel1.splitWords
	secondWords = npModel2.splitWords

	largerCollection = None
	smallerCollection = None
	if len(firstWords) < len(secondWords):
		largerCollection = secondWords
		smallerCollection = firstWords
	else:
		largerCollection = firstWords
		smallerCollection = secondWords

	mismatchCount = 0

	for i in range(0, len(largerCollection), 1):
		if i < len(smallerCollection):
			largerWord = largerCollection[i]
			smallerWord = smallerCollection[i]
			if (largerWord != smallerWord and
						npModel1.pronounType == npModel.nonePronounType and
						npModel2.pronounType == npModel.nonePronounType):
				mismatchCount += 1
		else:
			mismatchCount += 1

	return mismatchCount


def headNounsDifferRule(npModel1, npModel2):
	if npModel1.headNoun != npModel2.headNoun:
		return 1
	else:
		return 0


def subsumeRule(npModel1, npModel2):
	firstNp = str(npModel1).lower().strip()
	secondNp = str(npModel2).lower().strip()

	if len(firstNp) <= 1 or len(secondNp) <= 1:
		return 0

	if firstNp == it and secondNp == it:
		return -9999

	if npModel1.tag not in pronounTypes or npModel2.tag not in pronounTypes:
		return 0

	for badWord in badWords:
		if badWord in firstNp or badWord in secondNp:
			return 0

	if firstNp in secondNp:
		return -9999
	return 0


def iMeRule(npModel1, npModel2):
	norm1 = str(npModel1).lower().strip()
	norm2 = str(npModel2).lower().strip()

	if (norm1 == me and norm2 == i) or (norm1 == i and norm2 == me):
		return -9999

	return False


# not implementing for now
def specialThisRule(npModel1, npModel2):
	return 0


def findCorrectAntecedent(npModel, previousNps, sentences):
	# right now, just going to find the first np in the preceding sentence
	# get last noun phrase before current one
	scoringDict = {}

	distance = 0
	for previousNp in previousNps:
		distance += 1

		subsumeScore = subsumeRule(npModel, previousNp)
		reverseSubsumeScore = subsumeRule(previousNp, npModel)

		# we don't need to compare anymore if this is true
		# mismatch words score
		score1 = mismatchWordsRule(npModel, previousNp)
		# head noun differ score
		score2 = headNounsDifferRule(npModel, previousNp)
		# difference in position score, testing out heavy emphasis on it...
		score3 = distance
		# pronoun score
		score4 = pronounTypesRule(npModel, previousNp)
		# plurality score
		score5 = matchPlurality(npModel, previousNp)
		# proper names score
		score6 = properNamesRule(npModel, previousNp)
		# gender score
		score7 = matchGender(npModel, previousNp)
		# article score
		score8 = articleRule(previousNp)
		# wordmatching rule
		score9 = wordMatchingRule(npModel, previousNp)
		# special this rule
		specialThisScore = specialThisRule(npModel, previousNp)

		totalScore = score1 + score2 + score3 + score4 + score5 + score6 + score7 + score8 + score9

		totalScore = totalScore + subsumeScore
		totalScore = totalScore + reverseSubsumeScore
		totalScore = totalScore + iMeRule(npModel, previousNp)
		totalScore = totalScore + specialThisScore

		print str(npModel) + " => " + str(previousNp) + ":" + str(totalScore)
		scoringDict[totalScore] = previousNp

	od = collections.OrderedDict(sorted(scoringDict.items()))
	for item in od.items():
		if item[0] > 0:
			return None
		return item[1]
	return None


def updateDocumentWithCoreferences(docModel):
	previousItems = []
	sentences = []
	coreferencePairs = []

	for paragraph in docModel.paragraphs:
		for sentence in paragraph:
			for chunk in sentence:
				np = npModel.NpModel(chunk)

				if np.tag == nounPhraseKey:
					result = findCorrectAntecedent(np, previousItems, sentences)
					if result is not None:
						coreferencePairs.append((np, result))

					previousItems.insert(0, np)
			sentences.insert(0, sentence)

	return coreferencePairs