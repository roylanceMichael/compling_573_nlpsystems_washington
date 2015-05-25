__author__ = 'mroylance'

import os
import re
import sys
import extract
import attensity.semantic_server
import model.doc_model
import extract.topicReader
import extract.documentRepository
import extractionclustering.topicSummary
import extractionclustering.docModel
import extractionclustering.paragraph
import extractionclustering.sentence
import coherence.scorer
import coreference.rules
import pickle

cachePath = "../cache/docModelCacheOld"
summaryOutputPath = "../outputs"
reorderedSummaryOutputPath = summaryOutputPath + "_reordered"
evaluationOutputPath = "../results"
modelSummaryCachePath = "../cache/modelSummaryCache"
documentCachePath = "../cache/documentCache"
idfCachePath = "../cache/idfCache"
meadCacheDir = "../cache/meadCache"
rougeCacheDir = "../cache/rougeCache"

ss = attensity.semantic_server.SemanticServer()
configUrl = ss.configurations().config_url(7)

directories = ["/opt/dropbox/14-15/573/Data/models/devtest","/opt/dropbox/14-15/573/Data/models/training/2009","/opt/dropbox/14-15/573/Data/mydata"]

fileNames = []
for directory in directories:
	files = os.listdir(directory)
	for file in files:
		fileToPickle = os.path.join(directory, file)
		text = ""
		with open(fileToPickle, "r") as myFile:
			text = unicode(myFile.read(), errors='replace')

		parse = ss.parse()
		parse.process(text, configUrl)
		ext = attensity.extractions.Extractions.from_protobuf(parse.result)
		topicSummary = extractionclustering.topicSummary.TopicSummary()
		topicSummary.text = text

		newParagraph = extractionclustering.paragraph.Paragraph()
		newParagraph.text = text
		for extraction in ext.extractions():
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.KEYWORD_RESULTS:
				roots = {}
				for item in extraction.keyword_results.root:
					roots[item.id] = {"root": item.root, "word": item.word, "pos": item.pos}
				for item in extraction.keyword_results.location:
					roots[item.id]["sentence"] = item.sentence
				for key in roots:
					if "sentence" not in roots[key]:
						continue

					try:
						sentenceId = int(roots[key]["sentence"])
						root = str(roots[key]["root"])
						word = str(roots[key]["word"])
						pos = list(roots[key]["pos"])
						newParagraph.extractionKeywordResults.append((sentenceId, root, word, pos))
					except Exception:
						print "error happened"
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.FACT_RELATION:
				newParagraph.extractionFactRelations.append((extraction.fact_relation.fact_one, extraction.fact_relation.fact_two, extraction.fact_relation.text))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_SENTENCE:
				print "|||" + newParagraph.text[extraction.text_sentence.offset:extraction.text_sentence.offset + extraction.text_sentence.length] + "|||"
				newParagraph.extractionSentences.append((extraction.text_sentence.text_sentence_ID, extraction.text_sentence.offset, extraction.text_sentence.length))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.ENTITY:
				mid = ""
				if len(extraction.entity.search_info) > 0:
					mid = extraction.entity.search_info[0].machine_ID
				newParagraph.extractionEntities.append((extraction.entity.sentence_id, extraction.entity.display_text, extraction.entity.sem_tags, extraction.entity.domain_role, mid))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TRIPLE:
				newParagraph.extractionTriples.append((extraction.triple.sentence_ID, extraction.triple.t1.value, extraction.triple.t1.sem_tags, extraction.triple.t2.value, extraction.triple.t2.sem_tags, extraction.triple.t3.value, extraction.triple.t3.sem_tags))
				# print extraction
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.FACT:
				# print extraction
				newParagraph.extractionFacts.append((extraction.fact.sentence_ID, extraction.fact.element.text, extraction.fact.mode.text))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_PHRASE:
				# print extraction
				newParagraph.extractionTextPhrases.append((extraction.text_phrase.sentence_ID, extraction.text_phrase.head, extraction.text_phrase.root))

		sentences = {}
		sentenceNum = 0
		for sentence in newParagraph.extractionSentences:
			text = newParagraph.text
			actualSentence = text[sentence[1]:sentence[1] + sentence[2]]
			sentences[sentence[0]] = \
				extractionclustering.sentence.Sentence(
					actualSentence,
					sentence[0],
					sentenceNum,
					None)
			sentenceNum += 1

		for keywordResult in newParagraph.extractionKeywordResults:
			if keywordResult[0] in sentences:
				sentences[keywordResult[0]].keywordResults.append(keywordResult)

		for triple in newParagraph.extractionTriples:
			sentences[triple[0]].triples.append(triple)

		for entity in newParagraph.extractionEntities:
			sentences[entity[0]].entities.append(entity)

		for fact in newParagraph.extractionFacts:
			sentences[fact[0]].facts.append(fact)

		for phrase in newParagraph.extractionTextPhrases:
			sentences[phrase[0]].phrases.append(phrase)

		for sentence in sentences:
			topicSummary.sentences.append(sentences[sentence])

		# cache
		pickleFileName = os.path.join("../cache/goldCache", file)
		pickleFile = open(pickleFileName, 'wb')
		pickle.dump(topicSummary, pickleFile, pickle.HIGHEST_PROTOCOL)
		print "pickled " + pickleFileName
