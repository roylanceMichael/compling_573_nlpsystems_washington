__author__ = 'thomas'

import os

class EvaluationCompare:
	def __init__(self, resultsDir, meadCacheDir, rougeEvaluator):
		self.resultsDir = resultsDir
		self.meadCacheDir = meadCacheDir
		self.resultsFileName = os.path.join(self.resultsDir, "D3.results")
		self.meadStandardFileName = os.path.join(self.meadCacheDir, "evaluations", "standard.results")
		self.meadInitialFileName = os.path.join(self.meadCacheDir, "evaluations", "initial.results")
		self.meadRandomFileName = os.path.join(self.meadCacheDir, "evaluations", "random.results")
		self.rougeEvaluator = rougeEvaluator
		self.rouge = rougeEvaluator.rouge

	def printResultsFrom(self, resultsFileName, label):
		file = open(resultsFileName, 'r')
		buffer = file.read()
		resultsDict = self.rouge.output_to_dict(buffer)
		resultsString = "Results from: " + label + "\n"
		resultsString += "ROUGE-1: "
		resultsString += str(resultsDict['rouge_1_recall']) + " "
		resultsString += str(resultsDict['rouge_1_precision']) + " "
		resultsString += str(resultsDict['rouge_1_f_score']) + "\n"

		resultsString += "ROUGE-2: "
		resultsString += str(resultsDict['rouge_2_recall']) + " "
		resultsString += str(resultsDict['rouge_2_precision']) + " "
		resultsString += str(resultsDict['rouge_2_f_score']) + "\n"

		resultsString += "ROUGE-3: "
		resultsString += str(resultsDict['rouge_3_recall']) + " "
		resultsString += str(resultsDict['rouge_3_precision']) + " "
		resultsString += str(resultsDict['rouge_3_f_score']) + "\n"

		resultsString += "ROUGE-4: "
		resultsString += str(resultsDict['rouge_4_recall']) + " "
		resultsString += str(resultsDict['rouge_4_precision']) + " "
		resultsString += str(resultsDict['rouge_4_f_score']) + "\n"
		resultsString += "\n"

		file.close()
		return resultsString


	def getComparison(self):
		resultsBuffer = ""
		if os.path.exists(self.resultsFileName):
			resultsBuffer += self.printResultsFrom(self.resultsFileName, "System")

		if os.path.exists(self.resultsFileName):
			resultsBuffer += self.printResultsFrom(self.resultsFileName + "_reordered", "System_reordered")

		if os.path.exists(self.meadStandardFileName):
			resultsBuffer += self.printResultsFrom(self.meadStandardFileName, "MEAD Standard")

		if os.path.exists(self.meadInitialFileName):
			resultsBuffer += self.printResultsFrom(self.meadInitialFileName, "MEAD Initial")

		if os.path.exists(self.meadRandomFileName):
			resultsBuffer += self.printResultsFrom(self.meadRandomFileName, "MEAD Random")

		return resultsBuffer
