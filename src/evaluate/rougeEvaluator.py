__author__ = 'thomas'

from pyrouge import Rouge155
import os
import glob
import re
from subprocess import check_output

rougeConfigHeader = "<ROUGE_EVAL version=\"1.5.5\">\n"

rougeEvalEntryStart = \
"""
<EVAL ID=\"%s\">
<PEER-ROOT>
%s
</PEER-ROOT>
<MODEL-ROOT>
%s
</MODEL-ROOT>
<INPUT-FORMAT TYPE=\"SPL\">
</INPUT-FORMAT>
<PEERS>
<P ID=\"1\">%s</P>
</PEERS>
<MODELS>
"""

rougeEvalEntryModelEntryEnd = """
</MODELS>
</EVAL>
"""
rougeEvalEntryModelEntry = "<M ID=\"%s\">%s</M>\n"


rougeConfigFooter = """
</ROUGE_EVAL>
"""

rougeConfigFileName = "rouge_config.xml"

class RougeEvaluator():
	def __init__(self, rougeDir, modelSummaryDir, systemSummaryDir, modelSummaryCachePath):
		self.configFile = rougeConfigHeader
		self.rougeDir = rougeDir
		self.systemSummaryDir = os.path.abspath(systemSummaryDir)
		self.modelSummaryDir = os.path.abspath(modelSummaryDir)
		self.modelSummaryCachePath = os.path.abspath(modelSummaryCachePath)

	def addCompareToConfig(self, topic, modelSummaries):

		entry = rougeEvalEntryStart % (topic.id, self.systemSummaryDir, self.modelSummaryCachePath, topic.id)
		for modelSummaryFileName in modelSummaries:
			shortName = os.path.basename(modelSummaryFileName)
			entry += rougeEvalEntryModelEntry % (shortName[-1:], shortName)

		entry += rougeEvalEntryModelEntryEnd

		self.configFile += entry



	# this is because ROUGE doesn't appreciate non-utf8 characters
	def sanitizingCopy(self, inputFileName, outputFileName):
		outputFile = open(outputFileName, 'w')
		inputFile = open(inputFileName, 'r')
		for line in inputFile:
			outputFile.write(re.sub(r'[^\x00-\x7F]', ' ', line))
		outputFile.close()
		inputFile.close()

	def cacheModelSummaries(self, topics):
		try:
			os.stat(self.modelSummaryCachePath)
		except:
			os.mkdir(self.modelSummaryCachePath)
		n = 0
		for topic in topics:
			n += 1
			transformedTopicId = topic.docsetAId[:-3] + '-A'
			globString = os.path.join(self.modelSummaryDir, transformedTopicId + '.M.100.*')
			modelFiles = glob.glob(globString)
			for modelFile in modelFiles:
				self.sanitizingCopy(modelFile, modelFile.replace(self.modelSummaryDir, self.modelSummaryCachePath))
			self.addCompareToConfig(topic, modelFiles)
		self.configFile += rougeConfigFooter
		outputFile = open(rougeConfigFileName, 'w')
		outputFile.write(self.configFile)
		outputFile.close()


	def evaluate(self):

		abspath = os.path.abspath(self.rougeDir)
		rouge = Rouge155(abspath)
		# rouge = Rouge155(abspath,
		# 				 '-e /opt/dropbox/14-15/573/code/ROUGE/data -a -n 4 -x -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d')
		rouge.system_filename_pattern = 'D(\d+)[A-Z]'
		rouge.model_filename_pattern = 'D#ID#-A.M.100.[A-Z].[A-Z]'
		rouge.system_dir = os.path.abspath(self.systemSummaryDir)
		rouge.model_dir = os.path.abspath(self.modelSummaryCachePath)

		# output = rouge.convert_and_evaluate()

		rougeCommand = list()
		rougeCommand.append(os.path.join(self.rougeDir, "ROUGE-1.5.5.pl"))
		rougeCommand.append("-e")
		rougeCommand.append(os.path.join(self.rougeDir, "data"))
		rougeCommand.append("-a")
		rougeCommand.append("-n")
		rougeCommand.append("4")
		rougeCommand.append("-x")
		rougeCommand.append("-m")
		rougeCommand.append("-c")
		rougeCommand.append("95")
		rougeCommand.append("-r")
		rougeCommand.append("1000")
		rougeCommand.append("-f")
		rougeCommand.append("A")
		rougeCommand.append("-p")
		rougeCommand.append("0.5")
		rougeCommand.append("-t")
		rougeCommand.append("0")
		rougeCommand.append("-l")
		rougeCommand.append("100")
		rougeCommand.append("-s")
		rougeCommand.append("-d")

		print "Calling ROUGE with command: " + " ".join(rougeCommand)

		rougeCommand.append(os.path.abspath(rougeConfigFileName))

		output = check_output(rougeCommand)

		# print output
		outputDict = rouge.output_to_dict(output)

		return [output, outputDict]
