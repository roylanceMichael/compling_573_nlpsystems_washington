import os.path
import datetime
import re

docNoKey = "DOCNO"
dateTimeKey = "DATE_TIME"
docTypeKey = "DOCTYPE"
headerKey = "HEADER"
slugKey = "SLUG"
trailerKey = "TRAILER"
headlineKey = "HEADLINE"
pKey = "P"
bodyKey = "BODY"
textKey = "TEXT"
docKey = "DOC"


class Document:
	def __init__(self):
		"""
			Initilize the document
		"""
		self.docNo = ""
		self.dateTime = ""
		self.header = ""
		self.docType = ""
		self.slug = ""
		self.headline = ""
		self.trailer = ""
		self.body = ""
		self.comparableDateTime = None
		self.paragraphs = []

	def __str__(self):
		"""
			simple tostring method, used for the developer to see what the object looks like (need to cleanse single quotes)
		"""

		paragraphText = ""
		for paragraph in self.paragraphs:
			paragraphText += paragraph

		return """
		{
			docNo: '%s',
			dateTime: '%s',
			header: '%s',
			slug: '%s',
			headline: '%s',
			trailer: '%s',
			body: '%s',
			paragraphs: '%s'
		}
		""" % (self.docNo, self.dateTime, self.header, self.slug, self.headline, self.trailer, self.body, paragraphText)

	def getComparableDate(self):
		beginningOfTime = datetime.datetime(1970, 1, 1)

		try:
			beginningOfTime = datetime.datetime.strptime(re.sub("\\s+", "", self.dateTime)[0:10], "%Y-%m-%d")
		except:
			pass

		return beginningOfTime

	@staticmethod
	def build(objectDictionary):
		"""
			build the document object given a dictionary with string keys and array of strings values: { 'key', [ 'first', 'second' ]}
		"""

		newDocument = Document()

		if docNoKey in objectDictionary:
			for item in objectDictionary[docNoKey]:
				newDocument.docNo += item

		if docTypeKey in objectDictionary:
			for item in objectDictionary[docTypeKey]:
				newDocument.docType += item

		if dateTimeKey in objectDictionary:
			for item in objectDictionary[dateTimeKey]:
				newDocument.dateTime += item

		if headerKey in objectDictionary:
			for item in objectDictionary[headerKey]:
				newDocument.header += item

		if slugKey in objectDictionary:
			for item in objectDictionary[slugKey]:
				newDocument.slug += item

		if headlineKey in objectDictionary:
			for item in objectDictionary[headlineKey]:
				newDocument.headline += item

		if trailerKey in objectDictionary:
			for item in objectDictionary[trailerKey]:
				newDocument.trailer += item

		if pKey in objectDictionary:
			for item in objectDictionary[pKey]:
				newDocument.paragraphs.append(item)
		elif textKey in objectDictionary:
			for item in objectDictionary[textKey]:
				newDocument.paragraphs.append(item)

		if bodyKey in objectDictionary:
			for item in objectDictionary[bodyKey]:
				newDocument.body += item

		return newDocument

	@staticmethod
	def returnCharsFromDocument(filePath, seekToId):
		"""
			return the characters from a document
		"""

		docFile = open(filePath, 'r')

		if seekToId is not None:
			pos = 0
			prevpos = 0
			line = ""
			while seekToId not in line:
				prevpos = pos
				pos = docFile.tell()
				line = docFile.readline()

			if seekToId in line:
				if docNoKey in line:
					offset = prevpos - docFile.tell()
				else:
					offset = pos - docFile.tell()
				docFile.seek(offset, 1)
			else:
				raise IOError("Could not find topic " + seekToId + " in file " + filePath)

		while True:
			c = docFile.read(1)

			if not c:
				return

			yield c

	@staticmethod
	def returnCharsFromString(largeString):
		"""
			return the characters from a string
		"""
		for char in largeString:
			yield char

	@staticmethod
	def factoryFromIndexer(documentIndexer):
		if documentIndexer == None:
			return None

		index = 0
		actualString = ""
		for char in Document.returnCharsFromDocument(documentIndexer.fileName):
			if index >= documentIndexer.start and index <= documentIndexer.end:
				actualString += char
			elif index > documentIndexer.end:
				return Document.factory(actualString)

			index += 1

	@staticmethod
	def factoryForSpecificDocNo(inputFileName, docNo):
		"""
			build 1 document given an input and doc number
		"""

		charMethod = Document.returnCharsFromDocument

		tagStack = []
		currentTag = ""
		currentObject = {}

		seenOpeningTag = False
		seenClosingTag = False
		seenClosingXml = False
		workspace = ""

		foundDocNo = False

		for c in charMethod(inputFileName, docNo):
			# print c,
			if c == "<":
				seenOpeningTag = True
				tagStackLen = len(tagStack)

				if tagStackLen > 0:
					lastTag = tagStack[tagStackLen - 1]
					# check if we found the docno
					if lastTag == docNoKey and workspace.strip() == docNo:
						foundDocNo = True

					if lastTag in currentObject and foundDocNo:
						currentObject[lastTag].append(workspace)
					elif foundDocNo:
						currentObject[lastTag] = [workspace]

				currentTag = ""
				workspace = ""
			elif c == "/" and seenOpeningTag:
				seenClosingXml = True
			elif c == ">" and seenOpeningTag:
				# remove the last one
				if seenClosingXml and len(tagStack) > 0:
					tagStack.pop()
				else:
					if currentTag[:4] == "DOC " and docNo in currentTag:
						foundDocNo = True
						tagStack.append("DOC")
						currentObject[docNoKey] = [docNo]
					else:
						tagStack.append(currentTag)

				seenOpeningTag = False
				seenClosingXml = False
				seenClosingTag = False
				workspace = ""

				endedXmlDoc = len(tagStack) == 0
				if endedXmlDoc and foundDocNo:
					return Document.build(currentObject)
				elif endedXmlDoc:
					currentObject = {}
			elif seenOpeningTag:
				currentTag += c
			else:
				workspace += c
		return None

	@staticmethod
	def factory(input, isFile=False):
		"""
			build a single document given an input
		"""
		result = list(Document.factoryMultiple(input, isFile))

		if len(result) > 0:
			return result[0]
		return None

	@staticmethod
	def factoryMultiple(input, isFile=False, isSingle=True):
		"""
			build multiple documents given an input
		"""

		charMethod = Document.returnCharsFromString

		if isFile:
			charMethod = Document.returnCharsFromDocument

		tagStack = []
		currentTag = ""
		currentObject = {}

		seenOpeningTag = False
		seenClosingTag = False
		seenClosingXml = False
		workspace = ""

		for c in charMethod(input):
			if c == "<":
				seenOpeningTag = True

				tagStackLen = len(tagStack)

				if tagStackLen > 0:
					lastTag = tagStack[tagStackLen - 1]
					if lastTag in currentObject:
						currentObject[lastTag].append(workspace)
					else:
						currentObject[lastTag] = [workspace]

				currentTag = ""
				workspace = ""
			elif c == "/" and seenOpeningTag:
				seenClosingXml = True
			elif c == ">" and seenOpeningTag:
				# remove the last one
				if seenClosingXml and len(tagStack) > 0:
					tagStack.pop()
				else:
					tagStack.append(currentTag)

				seenOpeningTag = False
				seenClosingXml = False
				seenClosingTag = False
				workspace = ""

				if len(tagStack) == 0:
					yield Document.build(currentObject)

					# don't want to compute more than we have to...
					if isSingle:
						break

					currentObject = {}

			elif seenOpeningTag:
				currentTag += c
			else:
				workspace += c