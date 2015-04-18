import os.path

docNoKey = "DOCNO"
dateTimeKey = "DATE_TIME"
docTypeKey = "DOCTYPE"
headerKey = "HEADER"
slugKey = "SLUG"
trailerKey = "TRAILER"
headlineKey = "HEADLINE"
pKey = "P"
bodyKey = "BODY"

class DocumentIndexer:
	def __init__(self):
		"""
			Initilize the document
		"""
		self.docNo = ""
		self.fileName = ""
		self.start = -1
		self.end = -1

	def __str__(self):
		"""
			simple tostring method, used for the developer to see what the object looks like (need to cleanse single quotes)
		"""

		return """
		{
			docNo: '%s',
			fileName: '%s',
			start: '%s',
			end: '%s'
		}
		""" % (self.docNo, self.fileName, self.start, self.end)

	@staticmethod
	def build(objectDictionary, fileName, start, end):
		"""
			build the document object given a dictionary with string keys and array of strings values: { 'key', [ 'first', 'second' ]}
		"""

		newDocument = DocumentIndexer()

		if docNoKey in objectDictionary:
			for item in objectDictionary[docNoKey]:
				newDocument.docNo += item

		newDocument.fileName = fileName
		newDocument.start = start
		newDocument.end = end

		return newDocument

	@staticmethod
	def returnCharsFromDocument(filePath):
		"""
			return the characters from a document
		"""
		if os.path.isfile(filePath):
			with open(filePath) as f:
				while True:
					c = f.read(1)

					if not c:
						return

					yield c

	@staticmethod
	def factoryMultiple(input):
		"""
			build multiple documents given an input
		"""

		charMethod = DocumentIndexer.returnCharsFromDocument

		startIndex = 0
		currentIndex = -1

		tagStack = []
		currentTag = ""
		currentObject = {}

		seenOpeningTag = False
		seenClosingTag = False
		seenClosingXml = False
		workspace = ""

		for c in charMethod(input):
			currentIndex = currentIndex + 1
			if c == "<":
				seenOpeningTag = True

				tagStackLen = len(tagStack)

				if tagStackLen > 0:
					lastTag = tagStack[tagStackLen - 1]
					if lastTag in currentObject:
						currentObject[lastTag].append(workspace)
					else:
						currentObject[lastTag] = [ workspace ]

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
					yield DocumentIndexer.build(currentObject, input, startIndex, currentIndex)

					currentObject = {}
					startIndex = currentIndex

			elif seenOpeningTag:
				currentTag += c
			else:
				workspace += c