import xml.etree.ElementTree as ET
import json
import os
from os import listdir

topicQuery = ".//topic"

class Topic:
	def __init__(self):
		"""
			Initilize the topic
		"""
		self.id = ""
		self.category = ""
		self.title = ""
		self.docsetAId = ""
		self.docsetBId = ""
		self.docsetA = []
		self.docsetB = []

	def __str__(self):
			""" 
				simple tostring method, used for the developer to see what the object looks like (need to cleanse single quotes)
			"""

			docsetAText = ""
			for item in self.docsetA:
				docsetAText += item + ","

			docsetBText = ""
			for item in self.docsetB:
				docsetBText += item + ","

			return """
			{
				id: '%s',
				category: '%s',
				title: '%s',
				docsetAId: '%s',
				docsetBId: '%s',
				docsetA: '%s',
				docsetB: '%s'
			}
			""" % (self.id, self.category, self.title, self.docsetAId, self.docsetBId, docsetAText, docsetBText)

	@staticmethod
	def handleDocsetA(topic, element):
		topic.docsetAId = element.attrib["id"]

		for doc in element:
			topic.docsetA.append(doc.attrib["id"])

	@staticmethod
	def handleDocsetB(topic, element):
		topic.docsetBId = element.attrib["id"]

		for doc in element:
			topic.docsetB.append(doc.attrib["id"])

	@staticmethod
	def handleTitle(topic, element):
		topic.title = element.text

	@staticmethod
	def factoryMultiple(fileName):
		elementDictionary = { "title" : Topic.handleTitle, "docsetA": Topic.handleDocsetA, "docsetB":Topic.handleDocsetB  }

		xmlDocument = ET.parse(fileName)

		# get and parse
		root = xmlDocument.getroot()

		for element in root.findall(topicQuery):
			newTopic = Topic()
			newTopic.id = element.attrib["id"]
			newTopic.category = element.attrib["category"]

			for subElement in element:
				elementDictionary[subElement.tag](newTopic,subElement)

			yield newTopic