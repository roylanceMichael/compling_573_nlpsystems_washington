docNoKey = "DOCNO"
dateTimeKey = "DATE_TIME"
headerKey = "HEADER"
slugKey = "SLUG"
trailerKey = "TRAILER"
headlineKey = "HEADLINE"
pKey = "P"
bodyKey = "BODY"

class Document:
	def __init__(self):
		self.docNo = ""
		self.dateTime = ""
		self.header = ""
		self.slug = ""
		self.headline = ""
		self.trailer = ""
		self.body = ""
		self.paragraphs = []

	def __str__(self):

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

	@staticmethod
	def build(objectDictionary):
		newDocument = Document()

		if docNoKey in objectDictionary:
			for item in objectDictionary[docNoKey]:
				newDocument.docNo += item

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
			for item in objectDictionary[pKey]:
				newDocument.trailer += item

		if pKey in objectDictionary:
			for item in objectDictionary[pKey]:
				newDocument.paragraphs.append(item)

		if bodyKey in objectDictionary:
			for item in objectDictionary[bodyKey]:
				newDocument.body += item

		return newDocument

	@staticmethod
	def factory(filePath):
		with open(filePath) as f:
			tagStack = []
			currentTag = ""
			currentObject = {}

			seenOpeningTag = False
			seenClosingTag = False
			seenClosingXml = False


			workspace = ""
			while True:
				c = f.read(1)

				# end of file
				if not c:
					break

				if c == "<":
					seenOpeningTag = True

					tagStackLen = len(tagStack)

					if tagStackLen > 0:
						if tagStack[tagStackLen - 1] in currentObject:
							currentObject[tagStack[tagStackLen - 1]].append(workspace)
						else:
							currentObject[tagStack[tagStackLen - 1]] = [ workspace ]

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
						currentObject = {}

				elif seenOpeningTag:
					currentTag += c
				else:
					workspace += c