__author__ = 'mroylance'

import os
import re
import extract
import extract.topicReader
import extract.documentRepository
import model.doc_model
import model.asasEntityGrid
import model.entityGrid
import coherence.scorer
import coreference.rules
import svmlight
import itertools
import pickle
import operator
import extractionclustering.sentence
from evaluate.rougeEvaluator import RougeEvaluator
from evaluate.evaluationCompare import EvaluationCompare


cachePath = "../cache/docModelCache"
summaryOutputPath = "../outputs"
reorderedSummaryOutputPath = summaryOutputPath + "_reordered"
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"

rankModel = svmlight.read_model('../cache/svmlightCache/svmlightModel.dat')

rouge = RougeEvaluator("../ROUGE", "/opt/dropbox/14-15/573/Data/models/devtest", summaryOutputPath, modelSummaryCachePath, rougeCacheDir)

topics = []
for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
	topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository("/corpora/LDC/LDC02T31/", "/corpora/LDC/LDC08T25/data/", topics)

# load the cached docs
documentRepository.readFileIdDictionaryFromFileCache(documentCachePath)

# cache the model summaries
rouge.cacheModelSummaries(topics)

def getBestSummaryOrder(sentences, docIndex):
	permList = []

	testVectors = []

	permutations = itertools.permutations(sentences)
	for permutation in permutations:
		permList.append(permutation)
		grid = model.asasEntityGrid.AsasEntityGrid(permutation)
		featureVector = model.entityGrid.FeatureVector(grid, docIndex)
		vector = featureVector.getVector(1)
		testVectors.append(vector)

	predictions = svmlight.classify(rankModel, testVectors)

	maxInList = max(predictions)
	maxIndex = predictions.index(maxInList)
	print "reordering document(" + str(docIndex) + ")"
	bestOrder = permList[maxIndex]
	return bestOrder

##############################################################
# helper function for printing out buffers to files
##############################################################
def writeBufferToFile(path, buffer):
	outFile = open(path, 'w')
	outFile.write(buffer)
	outFile.close()
docIndex = 0

for fileName in os.listdir(cachePath):
	pickleFilePath = os.path.join(cachePath, fileName)
	if os.path.exists(pickleFilePath):
		pickleFile = open(pickleFilePath, 'rb')
		topicDictionary = pickle.load(pickleFile)

		allSentences = {}

		for docNo in topicDictionary:
			print docNo

			docModel = topicDictionary[docNo]
			for paragraph in docModel.paragraphs:
				sentences = {}
				sentenceNum = 0
				for sentence in paragraph.extractionSentences:
					text = paragraph.text
					actualSentence = text[sentence[1]:sentence[1] + sentence[2]]
					sentences[sentence[0]] = \
						extractionclustering.sentence.Sentence(
							actualSentence,
							sentence[0],
							sentenceNum,
							docModel)
					sentenceNum += 1

				for keywordResult in paragraph.extractionKeywordResults:
					if keywordResult[0] in sentences:
						sentences[keywordResult[0]].keywordResults.append(keywordResult)

				for triple in paragraph.extractionTriples:
					sentences[triple[0]].triples.append(triple)

				for entity in paragraph.extractionEntities:
					sentences[entity[0]].entities.append(entity)

				for fact in paragraph.extractionFacts:
					sentences[fact[0]].facts.append(fact)

				for phrase in paragraph.extractionTextPhrases:
					sentences[phrase[0]].phrases.append(phrase)

				for sentence in sentences:
					allSentences[sentences[sentence].uniqueId] = sentences[sentence]

		print "doing clustering now on summarization..."

		scoreDictionary = {}
		for uniqueSentenceId in allSentences:
			scoreDictionary[uniqueSentenceId] = 0
			compareSentence = allSentences[uniqueSentenceId]

			# for keywordResult in compareSentence.keywordResults:
				# print keywordResult
			print compareSentence.simple
			print "-------------------------"
			for otherUniqueSentenceId in allSentences:
				if uniqueSentenceId == otherUniqueSentenceId:
					continue

				score = compareSentence.distanceToOtherSentence(allSentences[otherUniqueSentenceId])
				scoreDictionary[uniqueSentenceId] += score

		maxSentences = 7
		sentenceIdx = 0
		uniqueSummaries = {}
		bestSentences = []
		for tupleResult in sorted(scoreDictionary.items(), key=operator.itemgetter(1), reverse=True):
			if sentenceIdx > maxSentences:
				break

			sentence = allSentences[tupleResult[0]]
			bestSentences.append(sentence)
			score = tupleResult[1]
			strippedSentence = re.sub("\s+", " ", sentence.simple)
			uniqueSummaries[strippedSentence] = None

			# print (strippedSentence, score)
			sentenceIdx += 1

		summary = ""
		for uniqueSentence in uniqueSummaries:
			summary += uniqueSentence + "\n"

		print summary
		if summary is not None:
			summaryFileName = summaryOutputPath + "/" + fileName
			summaryFile = open(summaryFileName, 'wb')
			summaryFile.write(summary)
			summaryFile.close()

		print "now calculating the best order..."
		bestOrder = getBestSummaryOrder(bestSentences, docIndex)

		summary = ""
		uniqueSummaries = {}
		for newSentence in bestOrder:
			actualText = re.sub("\s+", " ", newSentence.simple) + "\n"
			if actualText not in uniqueSummaries:
				uniqueSummaries[actualSentence] = None
				summary += actualText

		if summary is not None:
			summaryFileName = reorderedSummaryOutputPath + "/" + fileName
			summaryFile = open(summaryFileName, 'wb')
			summaryFile.write(summary)
			summaryFile.close()

		print summary

	docIndex += 1

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