import cPickle as pickle
from compressionCacheGen import Alligned

compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
#compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences', 'r'))

for a in c_corpus:

    sentence = a.__str__()

    a.triples = []
    a.entities = []
    a.entityScores = {}
    a.facts = []
    a.phrases = []

    """
    Ideally, I want to convert the above attencity outputs into word level features
    a.features[ word_index ] [ "in_a_X_relation_in_a_triple" ] = True
    sort of thing.
    Brandon can try to handle that himself, but Mike, who understands better what these
    are, would be better if he had time.
    """

pickle.dump(c_corpus, open(compressionCorpusCache+"c_Sentences_att_features", 'w'))
