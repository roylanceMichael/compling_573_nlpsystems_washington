import xml.etree.ElementTree as ET
import glob
import cPickle as pickle
#from nltk.tokenize import word_tokenize

class Alligned:
    def __init__(self, id, original, compressed):
        self.id = id

        #corpus is already whitespace delimited
        self.o_words = original.split()
        self.c_words = compressed.split()
        self.labels = list()

        c_pos = 0
        for o_pos in range(len(self.o_words)):
            if c_pos == len(self.c_words):
                self.labels.append('O')
            elif self.o_words[o_pos] == self.c_words[c_pos]:
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
cashefile = open("../cache/compressionCorpusCache/c_Sentences", 'w')
pickle.dump(c_corpus, cashefile)