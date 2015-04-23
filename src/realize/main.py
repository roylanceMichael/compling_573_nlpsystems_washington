import src.model.doc_model as doc_model
import json
import re
import src.extract.document as document
from src.selection.first_n import first_n
from src.order.order import in_order
from simple_realize import simple_realize
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

	print( simple_realize(in_order(first_n([doc_m])), 300))


if __name__ == '__main__':
	main()
