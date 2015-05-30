import cPickle as pickle
from corenlp import StanfordCoreNLP

classifierCachePath = "../cache/compressionCorpusCache/"
classifierFileName = "compressionClassifier"

selector, classifier = pickle.load(open(classifierCachePath+classifierFileName, 'rb'))

corenlp_dir = "/NLP_TOOLS/tool_sets/stanford-corenlp/stanford-corenlp-full-2015-04-20/"
parser = StanfordCoreNLP(corenlp_dir)
print("StanfordCoreNLP loaded")

def compress(sentence):
    print(type(sentence))
    return sentence


