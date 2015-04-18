import unittest
import extract.document


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

class DocumentTests(unittest.TestCase):
	def test_parseSingleDocument(self):
		# arrange
		# act
		foundDocument = extract.document.Document.factory(docXml)

		# assert
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

	def test_parseFromFile(self):
		# arrange
		# act

		# note, the first document is the same from above, this demonstrates reading it from a file
		fileName = "../doc/nyt/1998/19980601_NYT"
		foundDocument = None
		for document in extract.document.Document.factoryMultiple(fileName, True, False):
			foundDocument = document
			# just do one
			break

		# assert
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


def run():
    unittest.main()