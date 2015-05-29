import cPickle as pickle
from compressionCacheGen import Alligned
import model.idf
from model.idf import Idf
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import string

compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
#compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences', 'r'))

negation = ["not", "n't"]

stopWords = set(stopwords.words('english'))
punct = set(string.punctuation) | {"''", "``"}

idf = Idf("/home/thcrzy1/PycharmProjects/compling_573_nlpsystems_washington/cache/idfCache")
termFreq = defaultdict(int)

stemmer = SnowballStemmer('english')

for a in c_corpus:

    # add basic features

    # first/last words
    for i in range(1,6):
        if i < len(a):
            for x in range(i):
                a.features[x]["infirst"+str(i)] = True
                a.features[-1-x]["inlast"+str(i)] = True

    pos = [ x[1] for x in nltk.pos_tag(a.o_words) ]

    for i in range(len(a)):
        w = a.o_words[i]
        features = a.features[i]

        #capitalization
        if w.isupper():
            features["isupper"] = True
        elif w[0].isupper():
            features["firstupper"] = True

        w = w.lower()

        #word class
        if w in negation:
            features["negation"] = True
        elif w in punct:
            features["punct"] = True
        elif w in stopWords:
            features["stopWords"] = True

        #pos
        a.posfeatures[i]["pos_"+pos[i]] = True

        # compute the basic term frequencies of all words in paragraphs
        # for use in building corpus-wide quarry term frequency
        if w not in model.idf.stopWords:
            termFreq[w] += 1

        stem = stemmer.stem(w)
        suffix = ""
        if len(stem) < len(w) and w.startswith(stem):
            suffix = w[len(stem):]
        a.stemmed[i] = (stem, suffix)

# get max tfidf for scaling
maxtfidf = max( tf*idf.idf[w] for w, tf in termFreq.items() )

partitions = 5

# now add tfidf threshold features
for a in c_corpus:
    for i in range(len(a)):
        w = a.o_words[i].lower()
        features = a.features[i]

        tfidf = termFreq[w] * idf.idf[w]
        scaled = tfidf / maxtfidf * partitions
        for x in range(1,partitions):
            if tfidf > x:
                features[str(x*100/partitions)+"percenttfidf"] = True

example = c_corpus[0]

for i in range(len(example)):
    print(example.o_words[i])
    print(example.features[i])
    print(example.posfeatures[i])
    print(example.stemmed[i])
    print("")

pickle.dump(c_corpus, open(compressionCorpusCache+"c_Sentences_basic_features", 'w'))
