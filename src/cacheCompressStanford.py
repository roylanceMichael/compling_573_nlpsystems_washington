__author__ = 'gahlerbj'

import cPickle as pickle
from realize import compressionCacheGen
import sys
from corenlp import StanfordCoreNLP
import re

sys.modules['compressionCacheGen'] = compressionCacheGen

corenlp_dir = "/NLP_TOOLS/tool_sets/stanford-corenlp/stanford-corenlp-full-2015-04-20/"
parser = StanfordCoreNLP(corenlp_dir)

tree_re = re.compile(r"\(ROOT.*")

filePathToPickle = "../cache/compressionCorpusCache/c_Sentences_Stanford"
filePath = "../cache/compressionCorpusCache/c_Sentences"
fileHandle = open(filePath, "rb")
pickleFile = pickle.load(fileHandle)

cachedAligned = []

for aligned in pickleFile:
    if aligned is None:
        continue
    text = str(aligned)
    results = parser.raw_parse(text)

    aligned.tree = []
    aligned.dependencies = []

    for s in results['sentences']:
        aligned.tree.append(tree_re.search(s['parsetree']).group(0))
        aligned.dependencies += s['dependencies']


    cachedAligned.append(aligned)

pickleFile = open(filePathToPickle, 'wb')
pickle.dump(cachedAligned, pickleFile, pickle.HIGHEST_PROTOCOL)
print "pickled " + filePathToPickle
