__author__ = 'thomas'

from subprocess import check_output
import os



class MeadSummarizer:
	#
	# options for "method" are:
	#   standard - produce standard mead summaries
	#   initial - produce lead-based summary
	# 	random - produce random-sentence-based summary
	#
	def __init__(self, meadPath, baseOutputPath, clusterPath, method="standard"):
		self.meadPath = meadPath
		self.baseOutputPath = baseOutputPath
		self.clusterPath = clusterPath
		self.method = method
		self.outputPath = os.path.join(baseOutputPath, self.method)
		if not os.path.exists(self.outputPath):
			os.mkdir(self.outputPath)

	# writes summary to configured directory based on the type of summary being created.
	def summarizeAndWrite(self, topicId):

		fullClusterPath = os.path.join(os.path.abspath(self.clusterPath), topicId.strip())

		meadCommand = list()
		meadCommand.append(os.path.join(self.meadPath, "mead.pl"))
		if self.method == "initial":
			meadCommand.append("-LEADBASED")
		elif self.method == "random":
			meadCommand.append("-RANDOM")
		meadCommand.append("-w")
		meadCommand.append("-a")
		meadCommand.append("100")
		meadCommand.append(fullClusterPath)

		print "Calling MEAD with command: " + " ".join(meadCommand)

		output = check_output(meadCommand)
		inSents = output.split("\n")
		cleanOutput = ""
		for inSent in inSents:
			sent = inSent.strip()
			if sent != "":
				parts = sent.split("]")
				outSent = parts[1]
				cleanOutput += outSent.strip() + "\n"

		print cleanOutput

		self.saveToFile(cleanOutput, topicId)

	def saveToFile(self, cleanOutput, topicId):
		path = os.path.join(self.outputPath, topicId)
		file = open(path, 'w')
		file.write(cleanOutput)
		file.close()





