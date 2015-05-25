__author__ = 'thomas'

from textrazor import TextRazor

import re

mikeKey = "a40db69a54fa0905294e6b604b5dca251e9df8b912de4924d4254421"
thomasKey = "99cb513961595f163f4ab253a8aaf167970f8a49981e229a3c8505a0"

textRazor = TextRazor(api_key=thomasKey, extractors=["entities", "topics", "words", "dependency-trees"])

def getTextRazorInfo(sentences):
	text = "\n".join(sentences)
	cleanText = re.sub(r'[^\x00-\x7F]', ' ', text)
	results = textRazor.analyze(cleanText)
	return results