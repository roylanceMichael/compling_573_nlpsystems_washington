__author__ = 'mroylance'

import os
import sys
import extract
import attensity.semantic_server
import model.doc_model
import extract.topicReader
import extract.documentRepository
import coherence.scorer
import coreference.rules
import pickle

ss = attensity.semantic_server.SemanticServer()
configUrl = ss.configurations().config_url(4)

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
		coreference.rules.updateDocumentWithCoreferences(initialModel)
		coherence.scorer.determineDoc(initialModel)

		parse = ss.parse()

		for paragraph in initialModel.paragraphs:
			parse.process(str(paragraph), configUrl)
			ext = attensity.extractions.Extractions.from_protobuf(parse.result)

			for extraction in ext.extractions():
				if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_SENTENCE:
					paragraph.extractionSentences.append((extraction.text_sentence.text_sentence_ID, extraction.text_sentence.offset, extraction.text_sentence.length))
					print extraction
				if extraction.type == attensity.ExtractionMessage_pb2.Extraction.ENTITY:
					paragraph.extractionEntities.append((extraction.entity.sentence_id, extraction.entity.display_text, extraction.entity.sem_tags, extraction.entity.domain_role))
					print extraction
				if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TRIPLE:
					paragraph.extractionTriples.append((extraction.triple.sentence_ID, extraction.triple.t1.value, extraction.triple.t1.sem_tags, extraction.triple.t2.value, extraction.triple.t2.sem_tags, extraction.triple.t3.value, extraction.triple.t3.sem_tags))
					print extraction

			print str(paragraph)


		docModelCache[initialModel.docNo] = initialModel

	# cache
	pickleFileName = os.path.join("../cache/docModelCache", transformedTopicId)
	pickleFile = open(pickleFileName, 'wb')
	pickle.dump(docModelCache, pickleFile, pickle.HIGHEST_PROTOCOL)
	docModelCache = {}
