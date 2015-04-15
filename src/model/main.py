import doc_model
from src.extract.main import parseRecords
import json
import re
import src.extract.document as document
from os import listdir

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

def parseRecords(filePath):	
	
	for obj in document.Document.factory(filePath):
		return obj
	# let's just do one for now...
	return None


def main():
		
	doc_m = doc_model.Doc_Model(parseRecords("doc/nyt/1998/19980601_NYT"))
	
	txt = doc_m.paragraphs[0]
	print("text")
	print(txt)
	print("sentence")
	print(txt[0])
	print("chunk")
	print(txt[0][1])
	print("word")
	print(txt[0][1][0])
	print("stem")
	print(txt[0][1][0].stem)
	

if __name__ == '__main__':
    main()
