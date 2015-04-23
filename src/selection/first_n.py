def first_n(doc_list):
    for doc in doc_list:
        yield  doc.paragraphs[0][0]
        #for paragraph in doc.paragraphs:
        #    yield paragraph[0]
