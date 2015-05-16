__author__ = 'mroylance'

import os
import re
import extract
import extract.topicReader
import extract.documentRepository
import model.doc_model
import coherence.scorer
import coreference.rules
import pickle
import operator
import extractionclustering.sentence
from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare


cachePath = "../cache/docModelCache"
summaryOutputPath = "../outputs"
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"

rouge = RougeEvaluator("../ROUGE", "/opt/dropbox/14-15/573/Data/models/devtest", summaryOutputPath, modelSummaryCachePath, rougeCacheDir)

topics = []
for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
	topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository("/corpora/LDC/LDC02T31/", "/corpora/LDC/LDC08T25/data/", topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)

# cache the model summaries
rouge.cacheModelSummaries(topics)

##############################################################
# helper function for printing out buffers to files
##############################################################
def writeBufferToFile(path, buffer):
	outFile = open(path, 'w')
	outFile.write(buffer)
	outFile.close()

for fileName in os.listdir(cachePath):
	pickleFilePath = os.path.join(cachePath, fileName)
	if os.path.exists(pickleFilePath):
		pickleFile = open(pickleFilePath, 'rb')
		topicDictionary = pickle.load(pickleFile)

		allSentences = {}
		for docNo in topicDictionary:
			print docNo

			docModel = topicDictionary[docNo]
			sentences = {}
			sentenceNum = 0
			for sentence in docModel.extractionSentences:
				text = docModel.text
				actualSentence = text[sentence[1]:sentence[1] + sentence[2] + 1]
				sentences[sentence[0]] = \
					extractionclustering.sentence.Sentence(
						actualSentence,
						sentence[0],
						sentenceNum,
						docModel)
				sentenceNum += 1

			for triple in docModel.extractionTriples:
					sentences[triple[0]].triples.append(triple)
			for entity in docModel.extractionEntities:
					sentences[entity[0]].entities.append(entity)

			for fact in docModel.extractionFacts:
				sentences[fact[0]].facts.append(fact)

			for phrase in docModel.extractionTextPhrases:
				sentences[phrase[0]].phrases.append(phrase)

			for sentence in sentences:
				allSentences[sentences[sentence].uniqueId] = sentences[sentence]

		print "doing clustering now on summarization..."

		scoreDictionary = {}
		for uniqueSentenceId in allSentences:
			scoreDictionary[uniqueSentenceId] = 0

			compareSentence = allSentences[uniqueSentenceId]

			for otherUniqueSentenceId in allSentences:
				if uniqueSentenceId == otherUniqueSentenceId:
					continue

				score = compareSentence.distanceToOtherSentence(allSentences[otherUniqueSentenceId])
				scoreDictionary[uniqueSentenceId] += score

		maxSentences = 5
		sentenceIdx = 0
		uniqueSummaries = {}
		for tupleResult in sorted(scoreDictionary.items(), key=operator.itemgetter(1), reverse=True):
			if sentenceIdx > maxSentences:
				break

			sentence = allSentences[tupleResult[0]]
			score = tupleResult[1]
			strippedSentence = re.sub("\s+", " ", sentence.simple)
			uniqueSummaries[strippedSentence] = None

			print (strippedSentence, score)
			sentenceIdx += 1

		summary = ""
		for uniqueSentence in uniqueSummaries:
			summary += uniqueSentence + "\n"

		if summary is not None:
			summaryFileName = summaryOutputPath + "/" + fileName
			summaryFile = open(summaryFileName, 'wb')
			summaryFile.write(summary)
			summaryFile.close()

print "running the rouge evaluator"
evaluationResults = rouge.evaluate()
evaluation = evaluationResults[0]
writeBufferToFile(os.path.join(evaluationOutputPath, "D3.results"), evaluation)

# call the evaluation comparison routine.
# note:  this will only print t
# he summaries you have on your machine.
# 		 i.e. you should have run the meadSummaryGenerator.py first
# 		 (though defaults are checked into git)
comparator = EvaluationCompare(evaluationOutputPath, meadCacheDir, rouge)
comparison = comparator.getComparison()
print "\n" + comparison
writeBufferToFile(os.path.join(evaluationOutputPath, "results_compare.txt"), comparison)