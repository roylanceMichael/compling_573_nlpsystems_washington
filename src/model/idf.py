from nltk.corpus import reuters
from nltk.corpus import stopwords
from collections import defaultdict
import string
from math import log10
import cPickle as pickle

stopWords = set(stopwords.words('english')) | set(string.punctuation)

def generateIDF():
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
            idf[word] = 1 + idf.get(word, 1.0) # add one smoothing prevents divide by zero

    for word in idf.keys():
        idf[word] = logNumerator - log10(idf[word])

    return idf


def saveIDF(d):
    defaultValue = d.default_factory()
    print(defaultValue)
    d.default_factory = None
    pickle.dump((d,defaultValue), open("model/idf.dat", "wb"))

def loadIDF():
    d, defaultValue = pickle.load(open("model/idf.dat", "rb"))
    d.default_factory = lambda: defaultValue
    return d

idf = loadIDF()

if __name__ == '__main__':
    #saveIDF(generateIDF())
    idf = loadIDF()

    testWords = ["oil", "john", "president", "ivosnjkfe"]
    for word in testWords:
        print(word + ": " + str(idf[word]))
