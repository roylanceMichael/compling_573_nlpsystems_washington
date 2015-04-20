__author__ = 'thomas'

from pyrouge import Rouge155
import os
import shutil
import glob
import re


class RougeEvaluator():
	def __init__(self, rougeDir, modelSummaryDir, systemSummaryDir, modelSummaryCachePath):
		self.rougeDir = rougeDir
		self.systemSummaryDir = systemSummaryDir
		self.modelSummaryDir = modelSummaryDir
		self.modelSummaryCachePath = modelSummaryCachePath

	# this is because ROUGE doesn't appreciate non-utf8 characters
	def sanitizingCopy(self, inputFileName, outputFileName):
		outputFile = open(outputFileName, 'w')
		inputFile = open(inputFileName, 'r')
		for line in inputFile:
			outputFile.write(re.sub(r'[^\x00-\x7F]', ' ', line))
		outputFile.close()
		inputFile.close()

	def evaluate(self, topicId):
		modelTempDirName = self.modelSummaryCachePath + '/' + topicId
		try:
			os.stat(modelTempDirName)
		except:
			os.mkdir(modelTempDirName)

		globString = self.modelSummaryDir + '/' + topicId + '.M.100.*'
		modelFiles = glob.glob(globString)

		for modelFile in modelFiles:
			self.sanitizingCopy(modelFile, modelFile.replace(self.modelSummaryDir, modelTempDirName))

		abspath = os.path.abspath(self.rougeDir)
		rouge = Rouge155(abspath,
						 '-e /opt/dropbox/14-15/573/code/ROUGE/data -a -n 4 -x -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d')
		rouge.system_filename_pattern = '(' + topicId + ').OURS'
		rouge.model_filename_pattern = '#ID#.M.100.[A-Z].[A-Z]'
		rouge.system_dir = os.path.abspath(self.systemSummaryDir)
		rouge.model_dir = os.path.abspath(modelTempDirName)

		output = rouge.convert_and_evaluate(topicId)
		print output
		return output

		# output_dict = rouge.output_to_dict(output)
		#print(output_dict)