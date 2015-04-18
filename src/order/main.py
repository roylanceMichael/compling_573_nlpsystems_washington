import src.model.doc_model as doc_model
import json
import re
import src.extract.document as document
from src.select.first_n import first_n
from in_order import in_order
from os import listdir

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

def parseRecords(filePath):	
	
	for obj in document.Document.factoryMultiple(filePath, True, False):
		if obj:
			return obj
	# let's just do one for now...
	return None


def main():
		
	doc_m = doc_model.Doc_Model(parseRecords("doc/nyt/1998/19980601_NYT"))
	
	limit = 300
	current = 0
	for s in in_order(first_n([doc_m])):
		sentence = s.full
		current += len(sentence)
		if current > limit:
			break
		print(sentence)
	

if __name__ == '__main__':
    main()
