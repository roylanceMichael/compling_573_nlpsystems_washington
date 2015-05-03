__author__ = 'thomas'

import lxml.etree as etree
import os

header ="""<?xml version='1.0'?>
<CLUSTER LANG='ENG'>
"""

docEntry = "	<D DID=\'%s\' />\n"

footer = "</CLUSTER>\n"

class MeadDocumentCluster:
	def __init__(self, topic):
		self.topic = topic
		self.topicId = self.topic.id.strip()

	def write(self, filePath):
		filename = self.topicId + ".cluster"
		outputPath = os.path.join(filePath, self.topicId)
		if not os.path.exists(outputPath):
			os.mkdir(outputPath)
		path = os.path.join(outputPath, filename)
		outputText = header
		for document in self.topic.docsetA:
			outputText += docEntry % document

		outputText += footer
		file = open(path, 'w')
		file.write(outputText)
		file.close()
		