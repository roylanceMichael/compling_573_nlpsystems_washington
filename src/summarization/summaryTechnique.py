__author__ = 'thomas'


# abstract class for calling a summary technique.  should generate a dictionary of all sentences like:
# {Sentence.simple, score}
# score should be normalized from 0.0 to 1.0
#
# inherit from this class for new summary techniques.   Then just include the class in initialSummarizer.py
class SummaryTechnique(dict):
	def __init__(self, enabled, weight, docModels):
		super(SummaryTechnique, self).__init__()
		self.enabled = enabled
		self.weight = weight
		self.docModels = docModels

	def __getitem__(self, key):
		if not self.enabled:
			return 0.0
		else:
			try:
				return dict.__getitem__(self, key) * self.weight
			except KeyError:
				return 0.0

	def rankSentences(self):
		raise NotImplementedError("Please Implement this method")