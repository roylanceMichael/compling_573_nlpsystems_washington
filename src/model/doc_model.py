import nltk
import nltk.data
from nltk.tree import Tree
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
import string
from datetime import datetime

import src.extract.document

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = PorterStemmer().stem
chunking_grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP>+}                # chunk sequences of proper nouns
"""
chunker = nltk.RegexpParser(chunking_grammar)

stopWords = set(stopwords.words('english')) | set(string.punctuation)

nltk_v2 = nltk.__version__[0] == '2'

# implements comparisons based on .parent and .position_in_parent
class ParentCompare:
    def __lt__(self, other):
        if self.parent == other.parent:
            return self.position_in_parent < other.position_in_parent
        return self.parent < other.parent

    def __le__(self, other):
        if self.parent == other.parent:
            return self.position_in_parent < + other.position_in_parent
        return self.parent <= other.parent

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        if self.parent == other.parent:
            return self.position_in_parent == other.position_in_parent
        return False

    def __ne__(self, other):
        return not self == other


class Text(list, ParentCompare):
    def __init__(self, in_string, parent, position_in_parent):
        self.parent, self.position_in_parent = parent, position_in_parent
        self.full = in_string.strip()
        sentences = sentence_breaker.tokenize(self.full)

        # most articles start with a city and date followed by an underscore or --
        # the sentence breaker will just treat it as part of the first sentence
        if len(sentences) > 0:
            if " -- " in sentences[0]:
                sentences[0] = sentences[0].partition(" -- ")[2]
            elif " _ " in sentences[0]:
                sentences[0] = sentences[0].partition(" _ ")[2]

        list.__init__(self, (Sentence(sentences[x], self, x) for x in range(len(sentences))))

    def __str__(self):
        return self.full


class Sentence(list, ParentCompare):
    def __init__(self, in_string, parent, position_in_parent):
        self.parent, self.position_in_parent = parent, position_in_parent
        self.full = in_string

        # at this level we need to deside if we are doing full parsing or just chunking
        # I'll assume chunking for now because we need at least full NPs to figure out coreference
        # for now just assume every word is its own chunk

        tokenized = list(x for x in nltk.pos_tag(word_tokenize(self.full)) if len(x[0]) > 0)

        self.tree = chunker.parse(tokenized)
        #print(self.tree)

        list.__init__(self, (Chunk(self.tree[t], self, t) for t in range(len(self.tree))))

    def __str__(self):
        return self.full


class Chunk(list, ParentCompare):
    def __init__(self, tree, parent, position_in_parent):
        self.parent, self.position_in_parent = parent, position_in_parent

        if isinstance(tree, Tree):

            if nltk_v2:
                self.tag = tree.node  #nltk 2 version
            else:
                self.tag = tree.label()
            list.__init__(self, (Word(tree[x][0], tree[x][1], self, x) for x in range(len(tree))))
            self.full = " ".join(w.full for w in self)
        else:
            self.full, self.tag = tree
            list.__init__(self, [Word(self.full, self.tag, self, 0)])

        # coreference will occure at this level

    def __str__(self):
        return self.full


class Word(ParentCompare):
    def __init__(self, in_string, tag, parent, position_in_parent):
        self.parent, self.position_in_parent = parent, position_in_parent
        self.full = in_string
        #if len(in_string) == 0:
        #	print(parent.parent.tree)
        self.tag = tag
        self.stem = stemmer(in_string)

    def __str__(self):
        return self.full


class Doc_Model:
    def __init__(self, doc):
        self.docNo = doc.docNo
        if doc.dateTime.count(":") == 2:
            self.dateTime = datetime.strptime( doc.dateTime.strip(), "%Y-%m-%d %H:%M:%S" )
        else:
            self.dateTime = datetime.strptime( doc.dateTime.strip(), "%Y-%m-%d %H:%M" )

        self.header = Text(doc.header, self, -4)
        self.slug = Text(doc.slug, self, -3)
        self.headline = Text(doc.headline, self, -2)
        self.trailer = Text(doc.trailer, self, -1)
        self.body = Text(doc.body, self, 0)
        if len(doc.paragraphs) > 1:
            self.paragraphs = [Text(doc.paragraphs[x], self, x + 1) for x in range(len(doc.paragraphs))]
        else:
            #some documents have only tabbed paragraphs instead of xml delimited
            tab_split = ( x.strip() for x in doc.paragraphs[0].split("\t") )
            tab_split = [ x for x in tab_split if len(x) > 0 ]

            self.paragraphs = [Text(tab_split[x], self, x + 1) for x in range(len(tab_split))]

        # compute the term frequencies of all words in paragraphs
        # assuming we should use the quarry version of tf if we are using it
        # to rank sentences
        self.termFreq = defaultdict(lambda: 0.5)
        for word in self.words():
            if word.full not in stopWords:
                self.termFreq[word.full] = 1 + self.termFreq.get(word.full, 0.0)

        maxFreq = max(self.termFreq.items(), key = lambda x: x[1] )[1]
        for w in self.termFreq.keys():
            self.termFreq[w] = (self.termFreq[w] / maxFreq) + 0.5

    def __lt__(self, other):
        return isinstance(other, Doc_Model) and self.dateTime < other.dateTime

    def __le__(self, other):
        return isinstance(other, Doc_Model) and self.dateTime <= other.dateTime

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


    def sentences(self):
        for p in self.paragraphs:
            for s in p:
                yield s

    def chunks(self):
        for s in self.sentences():
            for c in s:
                yield c

    def words(self):
        for c in self.chunks():
            for w in c:
                yield w


class Cluster(list):
    def __init__(self, doclist):
        if isinstance(doclist[0], src.extract.document.Document):
            list.__init__(self, sorted(Doc_Model(x) for x in doclist) )
        else:
            list.__init__(self, sorted(doclist))

