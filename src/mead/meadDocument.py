__author__ = 'thomas'


import nltk
import lxml.etree as etree
import os

header = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE DOCSENT SYSTEM "/clair/tools/MEAD3/dtd/docsent.dtd">
<DOCSENT DID='%s' DOCNO='%s' LANG='ENG' CORR-DOC='%s.c'>
<BODY>
<HEADLINE><S PAR="1" RSNT="1" SNO="1">%s</S></HEADLINE>
<TEXT>
"""

sentenceEntry = "	<S PAR=\'2\' RSNT=\'%d\' SNO=\'%d\'>%s</S>\n"

footer = """</TEXT>
</BODY>
</DOCSENT>
"""


class MeadDocument:
	def __init__(self, topic, docInfo):
		self.docInfo = docInfo
		self.topic = topic
		self.topicId = self.topic.id.strip()
		self.docNo = self.docInfo.docNo.strip()
		self.sentences = nltk.sent_tokenize(' '.join(docInfo.paragraphs).replace('\n', ''))

	def write(self, filePath):
		filename = self.docNo + ".docsent"
		outputPath = os.path.join(filePath, self.topicId, "docsent")
		if not os.path.exists(outputPath):
			os.mkdir(outputPath)
		path = os.path.join(outputPath, filename)
		outputText = header % (self.docNo, self.docNo, self.docNo, self.docInfo.headline)
		sCounter = 0
		for sentenceText in self.sentences:
			sCounter += 1
			outputText += sentenceEntry % (sCounter, sCounter + 1, sentenceText)

		outputText += footer
		# x = etree.fromstring(outputText)
		# prettyOutputText = etree.tostring(x, pretty_print=True)

		file = open(path, 'w')
		file.write(outputText)
		file.close()
