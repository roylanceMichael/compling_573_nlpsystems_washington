__author__ = 'thomas'

# from pyrouge import Rouge155
import os
import glob
import re
from subprocess import check_output


# global templates
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

#
# class for doing evaluations using rouge.
# it used to use pyrouge for evaluation, but now it calls rouge directly
# the output is still sent to pyrouge to get a dictionary.
#
class RougeEvaluator():
	def __init__(self, rougeDir, modelSummaryDir, systemSummaryDir, modelSummaryCachePath, rougeCachePath):
		self.configFile = rougeConfigHeader
		self.rougeDir = rougeDir
		self.systemSummaryDir = os.path.abspath(systemSummaryDir)
		self.modelSummaryDir = os.path.abspath(modelSummaryDir)
		self.modelSummaryCachePath = os.path.abspath(modelSummaryCachePath)
		self.rougeCachePath = rougeCachePath
		self.rougeConfigFileName = os.path.join(self.rougeCachePath, "rouge_config.xml")
		self.abspath = os.path.abspath(self.rougeDir)
		# self.rouge = Rouge155(self.abspath)


	def reset(self):
		self.configFile = rougeConfigHeader

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
		outputFile = open(self.rougeConfigFileName, 'w')
		outputFile.write(self.configFile)
		outputFile.close()

	def evaluate(self):
		#self.rouge.system_filename_pattern = 'D(\d+)[A-Z]'
		#self.rouge.model_filename_pattern = 'D#ID#-A.M.100.[A-Z].[A-Z]'
		#self.rouge.system_dir = os.path.abspath(self.systemSummaryDir)
		#self.rouge.model_dir = os.path.abspath(self.modelSummaryCachePath˚)

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
		rougeCommand.append(os.path.abspath(self.rougeConfigFileName))

		print "Calling ROUGE with command: " + " ".join(rougeCommand)

		output = check_output(rougeCommand)

		# print output
		#outputDict = self.rouge.output_to_dict(output)

		return [output, {}]
