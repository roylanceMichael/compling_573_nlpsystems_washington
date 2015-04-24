from nltk.corpus import reuters
from nltk.corpus import stopwords
from collections import defaultdict
import string
from math import log10
import cPickle as pickle
import os


stopWords = set(stopwords.words('english')) | set(string.punctuation)


class Idf:
	def __init__(self, idfDataFile):

		if idfDataFile is None:
			self.idfDataFile = "model/idf.dat"
		else:
			self.idfDataFile = os.path.join(idfDataFile, 'idf.dat')

		self.idf = self.loadIDF()

	def generateIDF(self):
		files = reuters.fileids()
		logNumerator = log10(len(files))
		idf = defaultdict(lambda: logNumerator)

		for fileid in files:
			wordsInFile = set()
			for w in reuters.words(fileid):
				word = w.lower()
			if word not in stopWords:
				wordsInFile.add(word)

			for word in wordsInFile:
				idf[word] = 1 + idf.get(word, 1.0)  # add one smoothing prevents divide by zero

		for word in idf.keys():
			idf[word] = logNumerator - log10(idf[word])

		return idf

	def saveIDF(self, d):
		defaultValue = d.default_factory()
		print(defaultValue)
		d.default_factory = None
		pickle.dump((d, defaultValue), open(self.idfDataFile, "wb"))

	def loadIDF(self):
		d, defaultValue = pickle.load(open(self.idfDataFile, "rb"))
		d.default_factory = lambda: defaultValue
		return d


if __name__ == '__main__':
	# saveIDF(generateIDF())
	idfCalc = Idf()
	idf = idfCalc.loadIDF()

	testWords = ["oil", "john", "president", "ivosnjkfe"]
	for word in testWords:
		print(word + ": " + str(idf[word]))
