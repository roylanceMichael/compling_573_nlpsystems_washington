import src.model.doc_model as doc_model

def first_n(doc_list):
	for doc in doc_list:
		for paragraph in doc.paragraphs:
			yield paragraph[0]
