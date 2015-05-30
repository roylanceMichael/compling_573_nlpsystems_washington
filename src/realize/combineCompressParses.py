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
base = 'c_Sentences'
additions = ['c_Sentences_parsed', 'c_Sentences_Stanford']
output = 'c_Sentences_full_parsed'

c_corpus = pickle.load(open(compressionCorpusCache+base, 'rb'))

add = defaultdict(list)

for fp in additions:
    f = pickle.load(open(compressionCorpusCache+fp, 'rb'))
    for a in f:
        add[a.id].append(a)

for a in c_corpus:
    for b in add[a.id]:
        a.update(b)


example = c_corpus[0]
print(example.tree)
print(example.facts)
for i in range(len(example)):
    print(example.o_words[i])
    print("")

pickle.dump(c_corpus, open(compressionCorpusCache+output, 'w'))
