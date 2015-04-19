__author__ = 'thomas'

from pyrouge import Rouge155
import os
import shutil
import glob


class RougeEvaluator():
	def __init__(self, rougeDir, modelSummaryDir, systemSummaryDir, modelSummaryCachePath):
		self.rougeDir = rougeDir
		self.systemSummaryDir = systemSummaryDir
		self.modelSummaryDir = modelSummaryDir
		self.modelSummaryCachePath = modelSummaryCachePath

	def evaluate(self, topicId):
		modelTempDirName = self.modelSummaryCachePath + '/' + topicId
		try:
			os.stat(modelTempDirName)
		except:
			os.mkdir(modelTempDirName)

		globString = self.modelSummaryDir + '/' + topicId + '.M.100.*'
		modelFiles = glob.glob(globString)

		for modelFile in modelFiles:
			shutil.copy(modelFile, modelTempDirName)

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