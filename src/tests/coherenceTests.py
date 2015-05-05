__author__ = 'mroylance'
import unittest
import extract.document
import model.doc_model
import coherence.scorer


docXml = """
<DOC>
<DOCNO> NYT19980601.0001 </DOCNO>
<DOCTYPE> NEWS STORY </DOCTYPE>
<DATE_TIME> 1998-06-01 00:02 </DATE_TIME>
<HEADER>
A7753 &Cx1f; taf-z
u a &Cx13;  &Cx11;  BC-OBIT-LENIHAN-NYT &LR;      06-01 0290
</HEADER>
<BODY>
<SLUG> BC-OBIT-LENIHAN-NYT </SLUG>
<HEADLINE>
KENNETH J. LENIHAN, SOCIOLOGIST WHO STUDIED CAUSES OF RECIDIVISM,
DIES AT 69˚
</HEADLINE>
   (sw)
 By WOLFGANG SAXON
 c.1998 N.Y. Times News Service
<TEXT>
<P>
 John went to the bank to deposit his paycheck.
 He then took a train to Bill's car dealership.
 He needed to buy a car.
 The company he works for now isn't near any public transportation.
 He also wanted to talk to Bill about their softball league.
</P>
</TEXT>
</BODY>
<TRAILER>
NYT-06-01-98 0002EDT &QL;
</TRAILER>
</DOC>
"""


class CoherenceTests(unittest.TestCase):
	def test_parseSingleDocument(self):
		# arrange
		foundDocument = extract.document.Document.factory(docXml)
		docModel = model.doc_model.Doc_Model(foundDocument)

		# act
		for paragraph in docModel.paragraphs:
			coherence.scorer.determine(paragraph)


		# assert
		for paragraph in docModel.paragraphs:
			for sentence in paragraph:
				print str(sentence) + " " + str(sentence.coherenceTypes)

		self.assertTrue(True)