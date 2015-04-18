import unittest
import extract.topicReader

# dealing with this type of document
"""
<topic id = "D1001A" category = "2">

	<title> Columbine Massacre </title>

	<docsetA id = "D1001A-A">
		<doc id = "APW19990421.0284" />
		<doc id = "APW19990422.0082" />
		<doc id = "APW19990422.0095" />
		<doc id = "NYT19990423.0262" />
		<doc id = "NYT19990424.0231" />
		<doc id = "APW19990425.0023" />
		<doc id = "APW19990425.0114" />
		<doc id = "NYT19990425.0192" />
		<doc id = "APW19990427.0078" />
		<doc id = "APW19990428.0297" />
	</docsetA>

	<docsetB id = "D1001A-B">
		<doc id = "APW19990502.0104" />
		<doc id = "APW19990503.0128" />
		<doc id = "APW19990503.0161" />
		<doc id = "APW19990503.0260" />
		<doc id = "NYT19990503.0397" />
		<doc id = "XIE19990504.0020" />
		<doc id = "XIE19990504.0328" />
		<doc id = "APW19990506.0070" />
		<doc id = "APW19990510.0131" />
		<doc id = "APW19990511.0210" />
	</docsetB>
</topic>
"""

class TopicReaderTests(unittest.TestCase):
	def test_parseFromFile(self):
		# arrange
		# act
		fileName = "../doc/Documents/devtest/GuidedSumm10_test_topics.xml"
		foundTopic = None

		for topic in extract.topicReader.Topic.factoryMultiple(fileName):
			foundTopic = topic
			# just looking at one for now
			break

		# assert
		self.assertTrue( foundTopic != None )
		self.assertTrue( foundTopic.id.strip() ==  "D1001A" )
		self.assertTrue( foundTopic.category.strip() ==  "2" )
		self.assertTrue( foundTopic.title.strip() ==  "Columbine Massacre" )
		self.assertTrue( foundTopic.docsetAId.strip() ==  "D1001A-A" )
		self.assertTrue( foundTopic.docsetBId.strip() ==  "D1001A-B" )
		self.assertTrue( len(foundTopic.docsetA) ==  10 )
		self.assertTrue( len(foundTopic.docsetB) ==  10 )
		self.assertTrue( foundTopic.docsetA[0] ==  "APW19990421.0284" )
		self.assertTrue( foundTopic.docsetA[3] ==  "NYT19990423.0262" )
		self.assertTrue( foundTopic.docsetA[9] ==  "APW19990428.0297" )
		self.assertTrue( foundTopic.docsetB[0] ==  "APW19990502.0104" )
		self.assertTrue( foundTopic.docsetB[3] ==  "APW19990503.0260" )
		self.assertTrue( foundTopic.docsetB[9] ==  "APW19990511.0210" )

def run():
    unittest.main()