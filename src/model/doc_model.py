import nltk
import nltk.data
from nltk.tree import Tree
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
# from nltk.stem.snowball import SnowballStemmer

sentence_breaker = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = PorterStemmer().stem
chunking_grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP>+}                # chunk sequences of proper nouns
"""
chunker = nltk.RegexpParser(chunking_grammar)

nltk_v2 = nltk.__version__[0] == '2'

#implements comparisons based on .parent and .position_in_parent
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
		self.dateTime = doc.dateTime

		self.header = Text(doc.header, self, -4)
		self.slug = Text(doc.slug, self, -3)
		self.headline = Text(doc.headline, self, -2)
		self.trailer = Text(doc.trailer, self, -1)
		self.body = Text(doc.body, self, 0)
		self.paragraphs = [Text(doc.paragraphs[x], self, x + 1) for x in range(len(doc.paragraphs))]


