import unittest
import extract.document
import model.doc_model
import coreference.rules
import nltk.chunk


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
DIES AT 69
</HEADLINE>
   (sw)
 By WOLFGANG SAXON
 c.1998 N.Y. Times News Service
<TEXT>
<P>
 Eastern Airlines executives notified union leaders that the carrier wishes to discuss selective wage reductions on Feb. 3.
</P>
<P>
 Union representatives who could be reached said they hadn't decided whether they would respond.
</P>
<P>
 By proposing a meeting date, Eastern moved one step closer toward reopening current high-cost contract agreements with its unions.
 The proposal to meet followed an announcement Wednesday in which Philip Bakes, Eastern's president, laid out proposals to cut wages selectively an average of 29%.
 The airline's three major labor unions, whose contracts don't expire until year's end at the earliest, have vowed to resist the cuts.
</P>
<P>
 Nevertheless, one union official said he was intrigued by the brief and polite letter, which was hand-delivered by corporate security officers to the unions.
 According to Robert Callahan, president of Eastern's flight attendants union, the past practice of Eastern's parent, Houston-based Texas Air Corp., has involved confrontation and ultimatums to unions either to accept the carrier's terms or to suffer the consequences -- in this case, perhaps, layoffs.
</P>
<P>
 "Yesterday's performance was a departure," Mr. Callahan said, citing the invitation to conduct broad negotiations -- and the lack of a deadline imposed by management.
 "Frankly, it's a little mystifying."
</P>
</TEXT>
</BODY>
<TRAILER>
NYT-06-01-98 0002EDT &QL;
</TRAILER>
</DOC>
"""


class CoreferenceTests(unittest.TestCase):
    def test_parseSingleDocument(self):
        # arrange
        foundDocument = extract.document.Document.factory(docXml)
        docModel = model.doc_model.Doc_Model(foundDocument)

        # act
        pairs = coreference.rules.updateDocumentWithCoreferences(docModel)

        # assert
        for pair in pairs:
            print str(pair[0]) + " -> " + str(pair[1])

        self.assertTrue(True)