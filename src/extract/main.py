import xml.etree.ElementTree as ET
import json
import re
from os import listdir

recordDocQuery = ".//doc"
diseasesQuery = ".//diseases"

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

def insertRecords(folders, connection):
	cur = connection.cursor(buffered=True)
	
	# patient records
	for recordFolder in folders:

		for fileName in listdir(recordFolder):
			# read in entire file
			tree = ET.parse(recordFolder + "/" + fileName)

			# get and parse
			root = tree.getroot()

			for element in root.findall(recordDocQuery):
				valueTuple = (element.attrib["id"], reconstruct(element[0].text), recordFolder)

				cur.execute(recordInsertStatement, valueTuple)
				connection.commit()
				
				print "uploaded " + valueTuple[0]

def reconstruct(text):
	obeseRegex = "obes(?i)"
	obeseReplace = "#obese#"

	asthmaRegex = "asthm(?i)"
	asthmaReplace = "#asthma#"

	normalizedText = re.sub(whiteSpaceRegex, " ", text)

	words = []
	for word in normalizedText.split(" "):
		if re.search(obeseRegex, word):
			words.append(obeseReplace)
		elif re.search(asthmaRegex, word):
			words.append(asthmaReplace)
		else:
			words.append(word)

	return " ".join(words)