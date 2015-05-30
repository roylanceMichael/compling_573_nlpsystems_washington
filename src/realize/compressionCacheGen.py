import xml.etree.ElementTree as ET
import glob
import cPickle as pickle
#from nltk.tokenize import word_tokenize

class Alligned:
    def __init__(self, id, original, compressed):
        self.id = id

        # corpus is already whitespace delimited
        self.o_words = original.split()
        c_words = compressed.split()
        self.labels = list()

        c_pos = 0
        for o_pos in range(len(self.o_words)):
            if c_pos == len(c_words):
                self.labels.append('O')
            elif self.o_words[o_pos] == c_words[c_pos]:
                c_pos += 1
                if o_pos == 0 or self.labels[-1] == 'O':
                    self.labels.append('B')
                else:
                    self.labels.append('I')
            else:
                self.labels.append('O')

        """
        print(" ".join(self.o_words))
        print(" ".join(self.c_words))
        print(" ".join(self.labels))
        print("")
        """

        self.features = list(dict() for x in self.o_words)
        self.posfeatures = list(dict() for x in self.o_words)
        self.stemmed = list(None for x in self.o_words)

        self.triples = []
        self.entities = []
        self.entityScores = {}
        self.facts = []
        self.phrases = []

        self.tree = None
        self.dependencies = None

        self.treefeatures = list(dict() for x in self.o_words)
        self.dependfeatures = list(dict() for x in self.o_words)

    def update(self, otherAligned):
        for i in range(len(self.o_words)):
            if hasattr(otherAligned, 'features'):
                self.features[i].update(otherAligned.features[i])
            if hasattr(otherAligned, 'posfeatures'):
                self.posfeatures[i].update(otherAligned.posfeatures[i])
            if hasattr(otherAligned, 'stemmed'):
                self.stemmed[i] = otherAligned.stemmed[i]

            if hasattr(otherAligned, 'treefeatures'):
                self.treefeatures[i].update(otherAligned.treefeatures[i])
            if hasattr(otherAligned, 'dependfeatures'):
                self.dependfeatures[i].update(otherAligned.dependfeatures[i])

        if hasattr(otherAligned, 'triples') and len(otherAligned.triples):
            self.triples = otherAligned.triples
        if hasattr(otherAligned, 'entities') and len(otherAligned.entities):
            self.entities = otherAligned.entities
        if hasattr(otherAligned, 'entityScores'):
            self.entityScores.update(otherAligned.entityScores)
        if hasattr(otherAligned, 'facts') and len(otherAligned.facts):
            self.facts = otherAligned.facts
        if hasattr(otherAligned, 'phrases') and len(otherAligned.phrases):
            self.phrases = otherAligned.phrases

        if hasattr(otherAligned, 'tree') and otherAligned.tree:
            self.tree = otherAligned.tree
        if hasattr(otherAligned, 'dependencies') and otherAligned.dependencies:
            self.dependencies = otherAligned.dependencies


    def __str__(self):
        uniValue = (" ".join(self.o_words)).encode("utf-8")
        return str(uniValue)

    def compressed(self):
        return " ".join(self.o_words[i] for i in range(len(self.labels)) if self.labels[i] != 'O')

    def __len__(self):
        return len(self.o_words)

if __name__ == "__main__":

    c_corpus_dir = "/home/thcrzy1/compression_corpus/*.fixed"

    originals = dict()
    c_corpus = dict()

    for f in glob.glob(c_corpus_dir):
        print(f)
        tree = ET.parse(f)
        root = tree.getroot()
        for text in root:
            for s in text:
                id = s.attrib['id']
                sentence = s.text
                if s.tag == 'original':
                    originals[id] = sentence
                elif s.tag == 'compressed':
                    c_corpus[id] = Alligned(id, originals.pop(id), sentence)

        if len(originals):
            print(originals)
            originals.clear()

    c_corpus = list(c_corpus.values())
    print(str(len(c_corpus))+" sentences in compression corpus")

    compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
    #compressionCorpusCache = "../cache/compressionCorpusCache/"

    cashefile = open(compressionCorpusCache+"c_Sentences", 'w')
    pickle.dump(c_corpus, cashefile)