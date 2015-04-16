__author__ = 'thomas'


class RougeEvaluator():
    def __init__(self):
        self.rougeDirectory = rougeDirectory
        self.systemDir = systemDir
        self.modelDir = modelDir

    def evaluate(self, givenSummary):
        from pyrouge import Rouge155

        rouge = Rouge155("/home/thomas/projects/clms/ling573/src/RELEASE-1.5.5")
        rouge.system_dir = '/home/thomas/projects/clms/ling573/src/compling_573_nlpsystems_washington/outputs/nltkCheaterSummaries'
        rouge.model_dir = '/home/thomas/projects/clms/ling573/src/compling_573_nlpsystems_washington/outputs/goldStandardSummaries'
        rouge.system_filename_pattern = '(\w+).Frequency.txt'
        rouge.model_filename_pattern = '#ID#.First10.txt'
        output = rouge.convert_and_evaluate()
        print(output)
        return output

        #output_dict = rouge.output_to_dict(output)
        #print(output_dict)