import unittest
import extract.documentRepository

# D1009B
"""
	<docsetA id = "D1009B-A">
		<doc id = "NYT19981001.0493" />
		<doc id = "APW19990107.0206" />
		<doc id = "APW19990128.0158" />
		<doc id = "APW19990206.0079" />
		<doc id = "NYT19981215.0290" />
		<doc id = "NYT19980625.0509" />
		<doc id = "NYT19980627.0184" />
		<doc id = "APW19980709.0454" />
		<doc id = "NYT19980821.0418" />
		<doc id = "NYT19980904.0388" />
	</docsetA>
"""

rootFolder = "../doc/"

class DocumentRepositoryTests(unittest.TestCase):
	def test_simpleTopicGet(self):
		# arrange
		xmlFileLocation = "../doc/Documents/devtest/simpleTest.xml"
		topics = extract.topicReader.Topic.factoryMultiple(xmlFileLocation)
		docRepo = extract.documentRepository.DocumentRepository(rootFolder, rootFolder, topics)
		foundDocuments = []

		# act
		for foundDocument in docRepo.getDocumentsGroupedByTopic():
			foundDocuments.append(foundDocument)

		# assert
		self.assertTrue(len(foundDocuments) > 0)

	def test_simpleTopicGetTraining(self):
		# arrange
		xmlFileLocation = "../doc/Documents/training/2009/UpdateSumm09_test_topics.xml"
		topics = extract.topicReader.Topic.factoryMultiple(xmlFileLocation)
		docRepo = extract.documentRepository.DocumentRepository(rootFolder, rootFolder, topics)
		foundDocuments = []

		# act
		for foundDocument in docRepo.getDocumentsGroupedByTopic():
			foundDocuments.append(foundDocument)

		# assert
		self.assertTrue(len(foundDocuments) > 0)

	def test_simpleTopicGetFull(self):
		# arrange
		topicId = "D1009B"
		xmlFileLocation = "../doc/Documents/devtest/GuidedSumm10_test_topics.xml"
		topics = extract.topicReader.Topic.factoryMultiple(xmlFileLocation)
		docRepo = extract.documentRepository.DocumentRepository(rootFolder, rootFolder, topics)
		foundDocuments = []

		# act
		for foundDocument in docRepo.getDocumentsByTopic(topicId):
			foundDocuments.append(foundDocument)

		# assert
		self.assertTrue(len(foundDocuments) > 0)

	def test_simpleGet(self):
		# arrange
		documentId = "NYT19980601.0001"
		xmlFileLocation = "../doc/Documents/devtest/GuidedSumm10_test_topics.xml"
		topics = extract.topicReader.Topic.factoryMultiple(xmlFileLocation)
		docRepo =extract.documentRepository.DocumentRepository(rootFolder, rootFolder, topics)

		# act
		foundDocument = docRepo.getDocument(documentId)

		# assert
		self.assertTrue(foundDocument != None )
		self.assertTrue(foundDocument.docNo.strip() == "NYT19980601.0001" )
		self.assertTrue(foundDocument.docType.strip() == "NEWS STORY" )
		self.assertTrue(foundDocument.dateTime.strip() == "1998-06-01 00:02" )
		self.assertTrue(foundDocument.header.strip() == """A7753 &Cx1f; taf-z
u a &Cx13;  &Cx11;  BC-OBIT-LENIHAN-NYT &LR;      06-01 0290""" )
		self.assertTrue(foundDocument.slug.strip() == "BC-OBIT-LENIHAN-NYT" )
		self.assertTrue(foundDocument.headline.strip() == """KENNETH J. LENIHAN, SOCIOLOGIST WHO STUDIED CAUSES OF RECIDIVISM,
DIES AT 69""" )
		self.assertTrue(foundDocument.slug.strip() == "BC-OBIT-LENIHAN-NYT" )
		self.assertTrue(len(foundDocument.paragraphs) == 7)
		self.assertTrue(foundDocument.paragraphs[0].strip() == """NEW YORK _ Kenneth Joseph Lenihan, a New York research
sociologist who helped refine the scientific methods used in
criminology, died May 25 at his home in Manhattan. He was 69.""")
		self.assertTrue(foundDocument.paragraphs[1].strip() == """The cause was a heart attack, his family said.""")
		self.assertTrue(foundDocument.paragraphs[2].strip() == """Lenihan retired in 1995 as an associate professor of sociology
at John Jay College of Criminal Justice. He had joined the faculty
in 1980, after earlier stints as a researcher at Columbia
University's Bureau of Applied Social Research, the Vera Institute
of Justice in New York and the Bureau of Social Science Research in
Washington.""")
		self.assertTrue(foundDocument.paragraphs[3].strip() == """He brought his expertise to the study of recidivism rates among
criminal offenders. He conducted a study in Baltimore, called the
Life Project, for the U.S. Department of Labor in the early 1970s.""")
		self.assertTrue(foundDocument.paragraphs[4].strip() == """A large research project, it measured whether and how giving
jobs or money to recently released offenders would affect the
chances of their becoming repeaters. That project and further
studies formed the basis of a standard work in the field, which he
wrote with P. Rossi and D. Berk, ``Money, Work and Crime''
(Academic Press, 1980).""")
		self.assertTrue(foundDocument.paragraphs[5].strip() == """Lenihan was born in Queens, and graduated from Columbia's School
of General Studies in 1960. He also earned his M.A. and Ph.D. in
sociology at Columbia, the latter in 1974.""")
		self.assertTrue(foundDocument.paragraphs[6].strip() == """Lenihan is survived by two sons, Andrew of Miami, and William of
Manhattan; a daughter, Jean Lenihan of Seattle; four sisters,
Eileen McEwan of Houston, Moira Earhart of North Carolina, Jean
Dobson of Bay Shore, N.Y., and Sue Adams of Cape May, N.J.; and
three grandchildren.""")