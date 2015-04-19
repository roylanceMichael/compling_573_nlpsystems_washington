__author__ = 'thomas'

from pyrouge import Rouge155
import os

class RougeEvaluator():
    def __init__(self, rougeDir, modelSummaryDir, systemSummaryDir):
        self.rougeDir = rougeDir
        self.systemSummaryDir = systemSummaryDir
        self.modelSummaryDir = modelSummaryDir


    def evaluate(self, topicId, ):
        # rouge = Rouge155("/home/thomas/projects/clms/ling573/src/RELEASE-1.5.5")
        rouge = Rouge155(self.rougeDir)
        rouge.system_dir = os.path.abspath(self.systemSummaryDir)
        rouge.model_dir = os.path.abspath(self.modelSummaryDir)
        rouge.system_filename_pattern = '(' + topicId + ').M.100.[A-Z].[A-Z]'
        rouge.model_filename_pattern = '#ID#.OURS'
        output = rouge.convert_and_evaluate()
        print output
        return output

        #output_dict = rouge.output_to_dict(output)
        #print(output_dict)