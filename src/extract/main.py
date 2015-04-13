import json
import re
import document
from os import listdir

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

def parseRecords(folders):	
	
	for recordFolder in folders:

		for fileName in listdir(recordFolder):
			filePath = recordFolder + "/" + fileName
			for obj in document.Document.factory(filePath):
				print obj

			# let's just do one for now...
			return

def main():
	parseRecords(["doc/nyt/1998"])

if __name__ == '__main__':
    main()