import nltk
import nltk.data
from nltk.tree import Tree
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
import string
from datetime import datetime

import extract.document as document
import idf

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = PorterStemmer().stem
chunking_grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP|NNPS|NNS|NP>+}                # chunk sequences of proper nouns
"""
chunker = nltk.RegexpParser(chunking_grammar)


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

        self.wordNum = len(tokenized)

        self.tree = chunker.parse(tokenized)
        # print(self.tree)

        list.__init__(self, (Chunk(self.tree[t], self, t) for t in range(len(self.tree))))

    def __str__(self):
        return self.full

    def words(self):
        for c in self:
            for w in c:
                yield w


class Chunk(list, ParentCompare):
    def __init__(self, tree, parent, position_in_parent):
        self.parent, self.position_in_parent = parent, position_in_parent

        if isinstance(tree, Tree):

            if nltk_v2:
                self.tag = tree.node  # nltk 2 version
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
        # if len(in_string) == 0:
        # print(parent.parent.tree)
        self.tag = tag
        self.stem = stemmer(in_string)

    def __str__(self):
        return self.full


class Doc_Model:
    def __init__(self, doc):
        self.docNo = doc.docNo
        timeFormat = "%Y-%m-%d"
        if "/" in doc.dateTime:
            timeFormat = "%m/%d/%Y"
        colonCount = doc.dateTime.count(":")
        if colonCount == 2:
            timeFormat += " %H:%M:%S"
        elif colonCount == 1:
            timeFormat += " %H:%M"

        self.dateTime = datetime.strptime(doc.dateTime.strip(), timeFormat)

        self.header = Text(doc.header, self, -4)
        self.slug = Text(doc.slug, self, -3)
        self.headline = Text(doc.headline, self, -2)
        self.trailer = Text(doc.trailer, self, -1)
        self.body = Text(doc.body, self, 0)
        if len(doc.paragraphs) > 1:
            self.paragraphs = [Text(doc.paragraphs[x], self, x + 1) for x in range(len(doc.paragraphs))]
        else:
            # some documents have only tabbed paragraphs instead of xml delimited
            tab_split = (x.strip() for x in doc.paragraphs[0].split("\t"))
            tab_split = [x for x in tab_split if len(x) > 0]

            self.paragraphs = [Text(tab_split[x], self, x + 1) for x in range(len(tab_split))]

        # compute the basic term frequencies of all words in paragraphs
        # for use in building cluster-wide quarry term frequency
        self.termFreq = defaultdict(lambda: 0)
        for word in self.words():
            if word.full not in idf.stopWords:
                self.termFreq[word.full] += 1

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
        if isinstance(doclist[0], document.Document):
            list.__init__(self, sorted(Doc_Model(x) for x in doclist))
        else:
            list.__init__(self, sorted(doclist))

        # cluster-wide term frequency
        # assuming we should use the query version of tf if we are using it
        # to rank sentences, so a the queryTF exists to produce it

        self.termFreq = defaultdict(float)
        for doc in self:
            for w, f in doc.termFreq.items():
                self.termFreq[w] += f

        self._maxFreq = max(self.termFreq.items(), key=lambda x: x[1])[1]

    def getTF(self, word):
        return self.termFreq[word]

    def getTFIDF(self, word):
        return self.getTF(word) * idf.idf[word]

    def getQueryTF(self, word):
        return 0.5 + 0.5 * ( self.termFreq[word] / self._maxFreq ) if word in self.termFreq else 0.5

    def getQueryTFIDF(self, word):
        return self.getQueryTF(word) * idf.idf[word]

    def sentences(self):
        for doc in self:
            for s in doc.sentences():
                yield s

    def chunks(self):
        for doc in self:
            for c in doc.chunks():
                yield c

    def words(self):
        for doc in self:
            for w in doc.words():
                yield w


def main():
    doc = document.Document.factoryMultiple("/corpora/LDC/LDC02T31/apw/1998/19980601_APW_ENG", True, False).next()
    doc_m = Doc_Model(doc)

    print("date")
    print(doc_m.dateTime)

    txt = doc_m.paragraphs[0]
    print("text")
    print(txt)
    print("sentence")
    print(txt[0])
    print("chunk")
    print(txt[0][0])
    print("word")
    print(txt[0][0][0])
    print("stem")
    print(txt[0][0][0].stem)
    print("word term frequency")
    print(doc_m.termFreq[txt[0][0][0].full])


if __name__ == '__main__':
    main()