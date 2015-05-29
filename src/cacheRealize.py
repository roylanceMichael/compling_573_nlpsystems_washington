__author__ = 'mroylance'

import attensity
import cPickle as pickle
from realize import compressionCacheGen
import sys
sys.modules['compressionCacheGen'] = compressionCacheGen

filePathToPickle = "../cache/compressionCorpusCache/c_Sentences_parsed"
filePath = "../cache/compressionCorpusCache/c_Sentences_att_features"
fileHandle = open(filePath, "rb")
pickleFile = pickle.load(fileHandle)
ss = attensity.semantic_server.SemanticServer("http://192.168.1.11:8888")
configUrl = ss.configurations().config_url(3)

cachedAligned = []

for aligned in pickleFile:
	if aligned is None:
		continue
	text = str(aligned)

	parse = ss.parse()
	parse.process(unicode(text, errors='replace'), configUrl)
	ext = attensity.extractions.Extractions.from_protobuf(parse.result)

	for extraction in ext.extractions():
		print extraction
		if extraction.type == attensity.ExtractionMessage_pb2.Extraction.ENTITY:
			mid = ""
			if len(extraction.entity.search_info) > 0:
				mid = extraction.entity.search_info[0].machine_ID
			aligned.entities.append((extraction.entity.sentence_id, extraction.entity.display_text, extraction.entity.sem_tags, extraction.entity.domain_role, mid))
		if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TRIPLE:
			aligned.triples.append((extraction.triple.sentence_ID, extraction.triple.t1.value, extraction.triple.t1.sem_tags, extraction.triple.t2.value, extraction.triple.t2.sem_tags, extraction.triple.t3.value, extraction.triple.t3.sem_tags))
			# print extraction
		if extraction.type == attensity.ExtractionMessage_pb2.Extraction.FACT:
			# print extraction
			aligned.facts.append((extraction.fact.sentence_ID, extraction.fact.element.text, extraction.fact.mode.text))
		if extraction.type == attensity.ExtractionMessage_pb2.Extraction.TEXT_PHRASE:
			# print extraction
			aligned.phrases.append((extraction.text_phrase.sentence_ID, extraction.text_phrase.head, extraction.text_phrase.root))

	cachedAligned.append(aligned)

pickleFile = open(filePathToPickle, 'wb')
pickle.dump(cachedAligned, pickleFile, pickle.HIGHEST_PROTOCOL)
print "pickled " + filePathToPickle
