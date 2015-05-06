from collections import defaultdict

from model.doc_model import Sentence
from model.idf import stopWords
import numpy
from scipy import spatial
import time
import math

def cosine2(sentencePair, vocab=None):
	beg = time.time()
	counts = defaultdict(lambda: [0, 0])

	for i in (0, 1):
		for w in sentencePair[i].words():
			word = w.lower
			if vocab and word not in vocab:
				continue
			elif word in stopWords:
				continue

			counts[word][i] += 1

	magnitudes = [0.0, 0.0]
	dotProd = 0.0
	for value in counts.values():
		for i in (0, 1):
			magnitudes[i] += value[i] ** 2
		dotProd += value[0] * value[1]

	# can't do cosine similarity of one of the sentences has no in-vocab words
	# return 0 (completely dissimilar) in this case
	for i in (0, 1):
		if magnitudes[i] == 0.0:
			return 0
	cosSim = dotProd ** 2 / (magnitudes[0] * magnitudes[1])
	end = time.time() - beg
	return cosSim

def	cosine2b(sentencePair):
	beg = time.time()
	counts = defaultdict(lambda: [0, 0])
	vocab = []
	#  make vectors:
	for i in (0, 1):
		for w in sentencePair[i].words():
			word = w.full.lower()
			if word in stopWords:
				continue
			counts[word][i] += 1
			vocab.append(word)
	s1 = numpy.zeros(len(vocab))
	s2 = numpy.zeros(len(vocab))
	i = 0

	if len(vocab) == 0:
		return 0.0

	for word in vocab:
		s1[i] = float(counts[word][0])
		s2[i] = float(counts[word][1])
		i += 1

	cosSim = 1 - spatial.distance.cosine(s1, s2)
	end = time.time() - beg
	return cosSim


class DenseGraph(list):
	def __init__(self, sentences, simMeasure):
		self.sentences = sentences if isinstance(sentences, list) else list(sentences)
		self.remaining = set(range(len(self.sentences)))
		self._sNum = len(self.sentences)
		list.__init__(self)

	def __str__(self):
		return list.__str__(self)

	def getsim(self, sID0, sID1):
		raise NotImplemented()

	def setsim(self, sID0, sID1, value):
		raise NotImplemented()

	def applyfactor(self, sID0, sID1, factor):
		raise NotImplemented()

	# returns the sentence most similar to everything else,
	# then turns its sim scores with everything negative
	def pullinorder(self, pullfactor=-1.0):
		while len(self.remaining) > 0:
			sID = max(( sum(self.getsim(x, y) for y in range(self._sNum)), x ) for x in self.remaining)[1]

			for y in range(self._sNum):
				self.applyfactor(sID, y, pullfactor)

			yield self.sentences[sID]
			self.remaining.remove(sID)

	def simpleorder(self):
		f = open("/home/thcrzy1/Documents/matrix.txt", 'w')
		for score, sID in sorted((( sum(self.getsim(x, y) for y in range(self._sNum) if x!=y), x ) for x in self.remaining), reverse=True):
			f.write("{} {}\n".format(score, self.sentences[sID]))
			yield self.sentences[sID]
		f.flush()
		f.close()


class UnidirectedGraph(DenseGraph):
	def __init__(self, sentences, simMeasure):
		DenseGraph.__init__(self, sentences, simMeasure)
		for x in range(self._sNum):
			row = list()
			for y in range(x+1):
				row.append(simMeasure((self.sentences[x], self.sentences[y])))
			self.append(row)

	def getsim(self, sID0, sID1):
		if sID0 > sID1:
			return self[sID0][sID1]
		return self[sID1][sID0]

	def setsim(self, sID0, sID1, value):
		if sID0 > sID1:
			self[sID0][sID1] = value
		else:
			[sID1][sID0] = value

	def applyfactor(self, sID0, sID1, factor):
		if sID0 > sID1:
			self[sID0][sID1] *= factor
			self[sID0][sID1] = math.copysign(self[sID0][sID1], factor)
		else:
			self[sID1][sID0] *= factor
			self[sID1][sID0] = math.copysign(self[sID1][sID0], factor)


class DirectedGraph(DenseGraph):
	def __init__(self, sentences, simMeasure):
		DenseGraph.__init__(self, sentences, simMeasure)
		for x in range(self._sNum):
			row = list()
			for y in range(self._sNum):
				row.append(simMeasure((self.sentences[x], self.sentences[y])))
			self.append(row)

	def getsim(self, sID0, sID1):
		return self[sID0][sID1]

	def setsim(self, sID0, sID1, value):
		self[sID0][sID1] = value

	def applyfactor(self, sID0, sID1, factor):
		# change the score for both sID0 and sID1
		self[sID0][sID1] *= factor
		self[sID0][sID1] = math.copysign(self[sID0][sID1], factor)
		self[sID1][sID0] *= factor
		self[sID1][sID0] = math.copysign(self[sID1][sID0], factor)



if __name__ == '__main__':
	testSentences = (
	"Test sentence one.", "This is test sentence two.", "Sentence three.", "Here is the final sentence.")
	testSentences = tuple(Sentence(s, None, 0) for s in testSentences)
	simMeasure = cosine2b
	graph = UnidirectedGraph(testSentences, simMeasure)
	print(graph)
	print(graph.getsim(0, 2))
	print(graph.getsim(2, 0))
