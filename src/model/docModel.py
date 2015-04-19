import nltk
import nltk.data
# only on python 3.  we are using 2.7
# from nltk.sourcedstring import SourcedString
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
#from nltk.stem.snowball import SnowballStemmer

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = PorterStemmer().stem


class Word:
	def __init__(self, in_string, tag):
		self.full = in_string
		self.tag = tag
		self.stem = stemmer(in_string)

	def __str__(self):
		return self.full


class Chunk(list):
	def __init__(self, in_string, words, tag):
		self.full = in_string
		self.tag = tag
		self.extend(words)

		# coreference will occur at this level

	def __str__(self):
		return self.full


class Sentence(list):
	def __init__(self, in_string):
		self.full = in_string
		
		# at this level we need to decide if we are doing full parsing or just chunking
		# I'll assume chunking for now because we need at least full NPs to figure out coreference
		# for now just assume every word is its own chunk
		
		self.extend(Chunk(w, [Word(w, t)], t) for w, t in nltk.pos_tag(word_tokenize(self.full)))
		
	def __str__(self):
		return self.full


class Text(list):
    def __init__(self, inString):
        # self.full = SourcedString(in_string.strip(), "text body")
        self.full = inString.strip()
        self.extend(Sentence(x) for x in sentence_breaker.tokenize(self.full))

    def __str__(self):
        return self.full

class DocModel:
	def __init__(self, doc):
		self.docNo = doc.docNo
		self.dateTime = doc.dateTime
		
		self.header = Text(doc.header)
		self.slug = Text(doc.slug)
		self.headline = Text(doc.headline)
		self.trailer = Text(doc.trailer)
		self.body = Text(' '.join(doc.paragraphs).replace('\n', ''))
		self.paragraphs = [Text(x) for x in doc.paragraphs]


