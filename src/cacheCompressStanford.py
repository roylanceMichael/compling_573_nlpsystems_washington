__author__ = 'gahlerbj'

import cPickle as pickle
#import pickle
from realize import compressionCacheGen
import sys
from corenlp import StanfordCoreNLP
import re

sys.modules['compressionCacheGen'] = compressionCacheGen
from compressionCacheGen import Alligned

filePathToPickle = "../cache/compressionCorpusCache/c_Sentences_Stanford"
filePath = "../cache/compressionCorpusCache/c_Sentences"
fileHandle = open(filePath, "rb")
pickleFile = pickle.load(fileHandle)

print("pickle loaded")

corenlp_dir = "/NLP_TOOLS/tool_sets/stanford-corenlp/stanford-corenlp-full-2015-04-20/"
parser = StanfordCoreNLP(corenlp_dir)

print("Stanford loaded")

tree_re = re.compile(r"\(ROOT.*")

cachedAligned = []

for aligned in pickleFile:
    if aligned is None:
        continue
    text = unicode(str(aligned), errors='replace').encode('ascii', 'ignore')
    #
    try:
        results = parser.raw_parse(text)

        aligned.tree = []
        aligned.dependencies = []

        for s in results['sentences']:
            aligned.tree.append(tree_re.search(s['parsetree']).group(0))
            aligned.dependencies += s['dependencies']
     
     
    except:
    	print(text)
        print( "Unexpected error:", sys.exc_info()[0])

    cachedAligned.append(aligned)
    if len(cachedAligned) % 10 == 0:
    	print("parsed "+str(len(cachedAligned)))

pickleFile = open(filePathToPickle, 'wb')
pickle.dump(cachedAligned, pickleFile, pickle.HIGHEST_PROTOCOL)
print "pickled " + filePathToPickle
