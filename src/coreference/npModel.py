import re
import os

# this area will be where constant strings will exist
nominative = ["i", "he", "she", "we", "they"]
accusative = ["me", "him", "her", "us", "them", "whom"]
possessive = ["my", "your", "his", "our", "your", "their", "mine", "yours", "his", "hers", "ours", "yours", "theirs"]
reflexive = ["myself", "yourself", "himself", "herself", "itself", "ourselves", "themselves"]
ambiguous = ["you", "it"]

nonePronounType = "none"
nominativePronounType = "nomi"
accusativePronounType = "accu"
possessivePronounType = "poss"
reflexivePronounType = "refl"
ambiguousPronounType = "ambig"

pronounCheckingDict = {nominativePronounType: nominative, accusativePronounType: accusative,
					   possessivePronounType: possessive, reflexivePronounType: reflexive,
					   ambiguousPronounType: ambiguous}

pluralPronoun = ["we", "they", "us", "them", "our", "ours"]

noArticle = "none"
aArticle = "a"
anArticle = "an"
theArticle = "the"
someArticle = "some"
aRegex = "\s+a\s+"
anRegex = "\s+an\s+"
theRegex = "\s+the\s+"
someRegex = "\s+some\s+"

articleCheckingDict = {aRegex: aArticle, anRegex: anArticle, theRegex: theArticle, someRegex: someArticle}

capRegex = "[A-Z]"

male = "MALE"
female = "FEMALE"
unknown = "UNKNOWN"

maleNamesFile = "maleNames.txt"
maleNames = []
if os.path.isfile(maleNamesFile):
	with open(maleNamesFile) as f:
		name = f.readline()
		while name:
			maleNames.append(name)
			name = f.readline()

malePronouns = {"\b[Hh]e\b": None, "\b[Hh]is\b": None, "\b[Hh]imself\b": None, "\b[Hh]im\b": None}
femalePronouns = {"\b[Ss]he\b": None, "\b[Hh]er\b": None, "\b[Hh]erself\b": None, "\b[Hh]ers\b": None}
itPronoun = "\b[Ii]t\b"


class NpModel:
	def __init__(self, chunk):
		self.chunk = chunk
		self.tag = chunk.tag
		self.position_in_parent = chunk.position_in_parent
		self.normalizedPhrase = str(chunk).lower()
		self.splitWords = re.split("\s+", self.normalizedPhrase)
		self.pronounType = self.getPronounType()
		self.plurality = self.getPlurality()
		self.article = self.getArticle()
		self.properName = self.getProperName()
		self.gender = self.getGender()
		self.headNoun = self.getHeadNoun()

	def getPronounType(self):
		for key in pronounCheckingDict:
			for item in pronounCheckingDict[key]:
				if item in self.normalizedPhrase:
					return key

		return nonePronounType

	def getPlurality(self):
		if self.normalizedPhrase in pluralPronoun:
			return True

		lastIndex = len(self.splitWords)
		lastWord = self.splitWords[lastIndex - 1]
		lastWordLength = len(lastWord)

		if "'" not in lastWord and lastWord[lastWordLength - 1] == "s":
			return True
		return False

	def getArticle(self):
		for key in articleCheckingDict:
			if re.match(key, self.normalizedPhrase):
				return articleCheckingDict[key]

		return noArticle

	def getProperName(self):
		actualPhrase = str(self.chunk)

		splitWords = re.split("\s+", actualPhrase)

		allUpperCase = True
		for word in splitWords:
			if not re.match(capRegex, word):
				return False

		return True

	def getGender(self):
		for word in self.splitWords:
			if word.upper() in maleNames:
				return male

			for malePronoun in malePronouns:
				if re.match(malePronoun, word):
					return male

			for femalePronoun in femalePronouns:
				if re.match(femalePronoun, word):
					return female

			if re.match(itPronoun, word):
				return unknown

		return unknown

	def getHeadNoun(self):
		return self.splitWords[len(self.splitWords) - 1]

	def __str__(self):
		return self.normalizedPhrase

