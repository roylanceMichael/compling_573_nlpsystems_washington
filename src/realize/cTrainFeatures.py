import cPickle as pickle
from compressionCacheGen import Alligned
import model.idf
from model.idf import Idf
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tree import Tree
from collections import defaultdict
import string
import re

def getPathsToLeaves(tree, path=[], index=0):
    current = path+[tree.label()]
    for i in range(len(tree)):
        x=tree[i]
        if type(x) is Tree:
            for y in getPathsToLeaves(x, current, i):
                yield y
        else:
            yield (x, current, index)

def getDepths(d_tree, current=u'ROOT', depths=dict(), d = 0):
    if current not in depths:
        depths[current] = d
        for dep in d_tree[current]:
            getDepths(d_tree, dep[1], depths, d+1)
    return depths


compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
#compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences_full_parsed', 'r'))

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

    #pos = [ x[1] for x in nltk.pos_tag(a.o_words) ]

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
        #a.posfeatures[i]["pos_"+pos[i]] = True

        # compute the basic term frequencies of all words in paragraphs
        # for use in building corpus-wide quarry term frequency
        if w not in model.idf.stopWords:
            termFreq[w] += 1

        stem = stemmer.stem(w)
        suffix = ""
        if len(stem) < len(w) and w.startswith(stem):
            suffix = w[len(stem):]
        a.stemmed[i] = (stem, suffix)

    #Stanford tree features
    #print(a.tree)
    if a.tree:
        tree = Tree.fromstring(a.tree[0].encode('ascii', 'ignore'))
        #print(str(tree))
        paths = list(getPathsToLeaves(tree))
        #print(paths)
        for i in range(min(len(paths), len(a.o_words))):
            #print(paths[i][1])
            a.treefeatures[i]["tree_depth_"+str(len(paths[i][1]))] = True
            for x in range(0,2):
                a.treefeatures[i][str(x)+"_up_"+paths[i][1][-1-x]] = True
            for n in paths[i][1]:
                a.treefeatures[i]["tree_"+n] = True
            a.treefeatures[i][str(paths[i][2])+"_from_left"] = True
        #print(a.treefeatures[0])
    if a.dependencies:
        #make a tree out of it
        d_tree = defaultdict(list)
        mother_relations = defaultdict(list)
        daughter_relations = defaultdict(list)
        for dep in a.dependencies:
            d_tree[dep[1]].append((dep[0], dep[2]))
            mother_relations[dep[1]].append(dep[0])
            daughter_relations[dep[2]].append(dep[0])

        #now we can check depth and such
        #print(d_tree)
        depths = getDepths(d_tree, u'ROOT', dict(), 0)
        #print(depths)

        for i in range(len(a)):
            w = a.o_words[i]
            if w in depths:
                w_depth = depths[w]
                treefeatures = a.treefeatures[i]
                treefeatures["dep_depth_"+str(w_depth)] = True
                if w_depth > 3:
                    treefeatures["dep_depth_over_3"] = True
                if w_depth > 5:
                    treefeatures["dep_depth_over_5"] = True
            if w in mother_relations:
                for rel in mother_relations[w]:
                    treefeatures["dep_mother_"+rel] = True
            if w in daughter_relations:
                for rel in daughter_relations[w]:
                    treefeatures["dep_daughter_"+rel] = True








# get max tfidf for scaling
maxtfidf = max( tf*idf.idf[w] for w, tf in termFreq.items() )

partitions = 5

# now add tfidf threshold features
for a in c_corpus:
    for i in range(len(a)):
        w = a.o_words[i].lower()
        if w not in stopWords and w not in punct:
            features = a.features[i]

            tfidf = termFreq[w] * idf.idf[w]
            scaled = tfidf / maxtfidf * partitions
            for x in range(1,partitions):
                if scaled > x:
                    features[str(x*100/partitions)+"percenttfidf"] = True

example = c_corpus[0]

for i in range(len(example)):
    print(example.o_words[i])
    print(example.features[i])
    print(example.posfeatures[i])
    print(example.stemmed[i])
    print(example.treefeatures[i])
    print("")

pickle.dump(c_corpus, open(compressionCorpusCache+"c_Sentences_basic_features", 'w'))
