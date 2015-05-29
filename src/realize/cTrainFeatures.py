import cPickle as pickle
from compressionCacheGen import Alligned

#compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences', 'r'))

for a in c_corpus:

    # add basic features

    # first/last words
    for i in range(5):
        if i < len(a):
            a.features[i]["infirst"+str(i)] = True
            a.features[-i]["inlast"+str(i)] = True

