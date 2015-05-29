import cPickle as pickle
from compressionCacheGen import Alligned

#compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences', 'r'))

for a in c_corpus:

    sentence = str()

    a.triples = []
    a.entities = []
    a.entityScores = {}
    a.facts = []
    a.phrases = []

pickle.dump(c_corpus, open(compressionCorpusCache+"c_Sentences_att_features", 'w'))
