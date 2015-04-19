import nltk
import nltk.data
from nltk.tree import Tree
from nltk.sourcedstring import SourcedString, CompoundSourcedString
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
#from nltk.stem.snowball import SnowballStemmer

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = PorterStemmer().stem
chunking_grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP>+}                # chunk sequences of proper nouns
"""
chunker = nltk.RegexpParser(chunking_grammar)

class Text(list):
	def __init__(self, in_string, parent):
		self.parent = parent
		self.full = SourcedString(in_string.strip(), "text body")
		list.__init__(self, (Sentence(x, self) for x in sentence_breaker.tokenize(self.full)) )

	def __str__(self):
		return self.full

class Sentence(list):
	def __init__(self, in_string, parent):
		self.parent = parent
		self.full = in_string

		# at this level we need to deside if we are doing full parsing or just chunking
		# I'll assume chunking for now because we need at least full NPs to figure out coreference
		# for now just assume every word is its own chunk

		tokenized = list(x for x in nltk.pos_tag(word_tokenize(self.full)) if len(x[0])>0 )

		self.tree = chunker.parse( tokenized )
		#print(self.tree)

		list.__init__(self, (Chunk(t, self) for t in self.tree) )

	def __str__(self):
		return self.full

class Chunk(list):
	def __init__(self, tree, parent):
		self.parent = parent


		if isinstance(tree, Tree):

			self.tag = tree.node
			list.__init__(self, (Word(w,t, self) for w,t in tree ))
			if isinstance(self[0].full, SourcedString) and isinstance(self[-1].full, SourcedString) and not isinstance(self[0].full, CompoundSourcedString) and not isinstance(self[-1].full, CompoundSourcedString):
				# ):
				self.full = parent.full[self[0].full.begin:self[-1].full.end]
			else:
				self.full = " ".join(w.full for w in self)
		else:
			self.full, self.tag = tree
			list.__init__(self, [Word(self.full, self.tag, self)])

		# coreference will occure at this level

	def __str__(self):
		return self.full

class Word:
	def __init__(self, in_string, tag, parent):
		self.parent = parent
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
		self.dateTime = doc.dateTime

		self.header = Text(doc.header, self)
		self.slug = Text(doc.slug, self)
		self.headline = Text(doc.headline, self)
		self.trailer = Text(doc.trailer, self)
		self.body = Text(doc.body, self)
		self.paragraphs = [ Text(x, self) for x in doc.paragraphs ]