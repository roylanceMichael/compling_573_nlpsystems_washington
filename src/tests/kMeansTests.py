__author__ = 'mroylance'
import unittest
import extract.document
import model.doc_model
import kmeans.kMeans


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


otherDocXml = """
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
   NEW YORK _ Kenneth Joseph Lenihan, a New York research
sociologist who helped refine the scientific methods used in
criminology, died May 25 at his home in Manhattan. He was 69.
</P>
<P>
   The cause was a heart attack, his family said.
</P>
<P>
   Lenihan retired in 1995 as an associate professor of sociology
at John Jay College of Criminal Justice. He had joined the faculty
in 1980, after earlier stints as a researcher at Columbia
University's Bureau of Applied Social Research, the Vera Institute
of Justice in New York and the Bureau of Social Science Research in
Washington.
</P>
<P>
   He brought his expertise to the study of recidivism rates among
criminal offenders. He conducted a study in Baltimore, called the
Life Project, for the U.S. Department of Labor in the early 1970s.
</P>
<P>
   A large research project, it measured whether and how giving
jobs or money to recently released offenders would affect the
chances of their becoming repeaters. That project and further
studies formed the basis of a standard work in the field, which he
wrote with P. Rossi and D. Berk, ``Money, Work and Crime''
(Academic Press, 1980).
</P>
<P>
   Lenihan was born in Queens, and graduated from Columbia's School
of General Studies in 1960. He also earned his M.A. and Ph.D. in
sociology at Columbia, the latter in 1974.
</P>
<P>
   Lenihan is survived by two sons, Andrew of Miami, and William of
Manhattan; a daughter, Jean Lenihan of Seattle; four sisters,
Eileen McEwan of Houston, Moira Earhart of North Carolina, Jean
Dobson of Bay Shore, N.Y., and Sue Adams of Cape May, N.J.; and
three grandchildren.
</P>
</TEXT>
</BODY>
<TRAILER>
NYT-06-01-98 0002EDT &QL;
</TRAILER>
</DOC>
"""



class KMeansTests(unittest.TestCase):
    def test_parseSingleDocument(self):
        # arrange
        foundDocument = extract.document.Document.factory(docXml)
        otherFoundDocument = extract.document.Document.factory(otherDocXml)
        docModel = model.doc_model.Doc_Model(foundDocument)
        otherDocModel = model.doc_model.Doc_Model(otherFoundDocument)

        kMeans = kmeans.kMeans.KMeans([docModel, otherDocModel ])

        # act
        highestParagraphs = kMeans.buildDistances()  # assert
        for paragraphResult in highestParagraphs:
            print "----------------"
            print str(paragraphResult[0]) + " " + str(paragraphResult[1])

        self.assertTrue(True)