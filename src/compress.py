import cPickle as pickle
import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tree import Tree
from collections import defaultdict
import string
import re
import sys

import model.idf
from model.idf import Idf

from extractionclustering.sentence import Sentence
from corenlp import StanfordCoreNLP

classifierCachePath = "../cache/compressionCorpusCache/"
classifierFileName = "compressionClassifier"

vec, selector, classifier = pickle.load(open(classifierCachePath+classifierFileName, 'rb'))

"""
corenlp_dir = "/NLP_TOOLS/tool_sets/stanford-corenlp/stanford-corenlp-full-2015-04-20/"
parser = StanfordCoreNLP(corenlp_dir)
tree_re = re.compile(r"\(ROOT.*")
print("StanfordCoreNLP loaded")
# needed for tree features
"""

def getPathsToLeaves(tree, path=[], index=0):
    current = path+[tree.label()]
    for i in range(len(tree)):
        x=tree[i]
        if type(x) is Tree:
            for y in getPathsToLeaves(x, current, i):
                yield y
        else:
            yield (x, current, index)

negation = ["not", "n't"]

stopWords = set(stopwords.words('english'))
punct = set(string.punctuation) | {"''", "``"}

idf = Idf("/home/thcrzy1/PycharmProjects/compling_573_nlpsystems_washington/cache/idfCache")
termFreq = defaultdict(int)

stemmer = SnowballStemmer('english')

def compress(sentence):
    text = sentence.simple
    words = word_tokenize(text)
    w_features = [dict() for w in words]
    stemmed = [None for w in words]

    labels = list()


    # add basic features

    # first/last words
    for i in range(1,6):
        if i < len(words):
            for x in range(i):
                w_features[x]["infirst"+str(i)] = True
                w_features[-1-x]["inlast"+str(i)] = True

    #pos = [ x[1] for x in nltk.pos_tag(a.o_words) ]

    for i in range(len(words)):
        w = words[i]
        features = w_features[i]


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
        #a.posfeatures[i]["pos_"+pos[i]] = True

        # compute the basic term frequencies of all words in paragraphs
        # for use in building corpus-wide quarry term frequency
        if w not in model.idf.stopWords:
            termFreq[w] += 1

        stem = stemmer.stem(w)
        suffix = ""
        if len(stem) < len(w) and w.startswith(stem):
            suffix = w[len(stem):]
        stemmed[i] = (stem, suffix)

        features["stem_"+stemmed[i][0]] = True
        features["affix_"+stemmed[i][1]] = True


    #Stanford tree features
    text = text.encode('ascii', 'ignore')

    """
    tree = None
    dependencies = None

    try:
        results = parser.raw_parse(text)
        tree = []
        dependencies = []

        for s in results['sentences']:
            tree.append(tree_re.search(s['parsetree']).group(0))
            dependencies += s['dependencies']


    except:
        print(text)
        print( "Unexpected error:", sys.exc_info()[0])


    #print(a.tree)
    if tree:
        tree = Tree.fromstring(tree[0].encode('ascii', 'ignore'))
        #print(str(tree))
        paths = list(getPathsToLeaves(tree))
        #print(paths)
        for i in range(min(len(paths), len(words))):
            #print(paths[i][1])
            w_features[i]["tree_depth_"+str(len(paths[i][1]))] = True
            for x in range(0,2):
                w_features[i][str(x)+"_up_"+paths[i][1][-1-x]] = True
            for n in paths[i][1]:
                w_features[i]["tree_"+n] = True
            a.treefeatures[i][str(paths[i][2])+"_from_left"] = True
        #print(a.treefeatures[0])
    """

    # get max tfidf for scaling
    maxtfidf = max( tf*idf.idf[w] for w, tf in termFreq.items() )

    partitions = 5

    # now add tfidf threshold features
    for i in range(len(words)):
        w = words[i].lower()
        if w not in stopWords and w not in punct:
            features = w_features[i]

            tfidf = termFreq[w] * idf.idf[w]
            scaled = tfidf / maxtfidf * partitions
            for x in range(1,partitions):
                if tfidf > x:
                    features[str(x*100/partitions)+"percenttfidf"] = True

    #for f in w_features:
    #    print(f)


    # add previous features and classify
    for i in range(len(words)):

        f = w_features[i].copy()

        for prev in range(2):
            if i > prev:
                prevstring = "prev"+str(prev)+"_"
                f[prevstring+labels[-1-prev]] = True

                prevfeatures = w_features[i-1-prev]
                for k,v in prevfeatures.items():
                    if not k.startswith("in"):
                        f[prevstring+k] = v

        #print("with prev:")
        #print(f)

        # classify
        vector = vec.transform(f)
        vector = selector.transform(vector)
        result = classifier.predict(vector)
        l = result[0]
        #print(l)

        labels.append(l)

    # use labels to clear out
    print(labels)

    retained_words = list()
    for i in range(len(labels)):
        if labels[i] != 'O':
            retained_words.append(words[i])

    sentence.simple = " ".join(retained_words)

    return sentence


if __name__ == "__main__":
    pass


