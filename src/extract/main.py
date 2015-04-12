import xml.etree.ElementTree as ET
import json
import re
from os import listdir

recordDocQuery = ".//DOC"
diseasesQuery = ".//diseases"

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

def parseRecords(folders):	
	# patient records
	for recordFolder in folders:

		for fileName in listdir(recordFolder):
			# read in entire file
			print recordFolder + "/" + fileName
			parser = ET.XMLParser()
			parser.parser.UseForeignDTD(True)
			tree = ET.parse(recordFolder + "/" + fileName, parser=parser)

			# get and parse
			root = tree.getroot()

			for element in root.findall(recordDocQuery):
				print "HELLO"

def main():
	parseRecords(["doc/nyt/1998"])

if __name__ == '__main__':
    main()