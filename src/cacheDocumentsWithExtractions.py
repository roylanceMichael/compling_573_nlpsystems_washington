__author__ = 'mroylance'

import os
import re
import sys
import extract
import attensity.semantic_server
import model.doc_model
import extract.topicReader
import extract.documentRepository
import extractionclustering.docModel
import coherence.scorer
import coreference.rules
import pickle

ss = attensity.semantic_server.SemanticServer()
configUrl = ss.configurations().config_url(7)

topics = []
for topic in extract.topicReader.Topic.factoryMultiple("../doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
	topics.append(topic)

documentRepository = extract.documentRepository.DocumentRepository("/corpora/LDC/LDC02T31/", "/corpora/LDC/LDC08T25/data/", topics)

# load and cache the docs if they are not loaded.  just get them if they are.
docModelCache = {}
for topic in topics:
	transformedTopicId = topic.docsetAId[:-3] + '-A'
	print "caching topicId: " + transformedTopicId
	# let's get all the documents associated with this topic

	# get the doc objects, and build doc models from them
	for foundDocument in documentRepository.getDocumentsByTopic(topic.id):
		initialModel = model.doc_model.Doc_Model(foundDocument)
		docNo = initialModel.docNo
		coreference.rules.updateDocumentWithCoreferences(initialModel)
		coherence.scorer.determineDoc(initialModel)

		parse = ss.parse()

		wholeDocument = ""
		for paragraph in initialModel.paragraphs:
			cleansedStr = re.sub("\s+", " ", str(paragraph))
			wholeDocument += cleansedStr + " "

		docModel = extractionclustering.docModel.DocModel()
		docModel.text = wholeDocument

		parse.process(wholeDocument, configUrl)
		ext = attensity.extractions.Extractions.from_protobuf(parse.result)

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

					sentenceId = int(roots[key]["sentence"])
					root = str(roots[key]["root"])
					word = str(roots[key]["word"])
					pos = list(roots[key]["pos"])
					docModel.extractionKeywordResults.append((sentenceId, root, word, pos))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.FACT_RELATION:
				docModel.extractionFactRelations.append((extraction.fact_relation.fact_one, extraction.fact_relation.fact_two, extraction.fact_relation.text))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_SENTENCE:
				docModel.extractionSentences.append((extraction.text_sentence.text_sentence_ID, extraction.text_sentence.offset, extraction.text_sentence.length))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.ENTITY:
				mid = ""
				if len(extraction.entity.search_info) > 0:
					mid = extraction.entity.search_info[0].machine_ID
				docModel.extractionEntities.append((extraction.entity.sentence_id, extraction.entity.display_text, extraction.entity.sem_tags, extraction.entity.domain_role, mid))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TRIPLE:
				docModel.extractionTriples.append((extraction.triple.sentence_ID, extraction.triple.t1.value, extraction.triple.t1.sem_tags, extraction.triple.t2.value, extraction.triple.t2.sem_tags, extraction.triple.t3.value, extraction.triple.t3.sem_tags))
				# print extraction
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.FACT:
				# print extraction
				docModel.extractionFacts.append((extraction.fact.sentence_ID, extraction.fact.element.text, extraction.fact.mode.text))
			if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_PHRASE:
				# print extraction
				docModel.extractionTextPhrases.append((extraction.text_phrase.sentence_ID, extraction.text_phrase.head, extraction.text_phrase.root))

		print str(wholeDocument)
		docModelCache[docNo] = docModel

	# cache
	pickleFileName = os.path.join("../cache/docModelCache", topic.id)
	pickleFile = open(pickleFileName, 'wb')
	pickle.dump(docModelCache, pickleFile, pickle.HIGHEST_PROTOCOL)
	docModelCache = {}
