import src.model.doc_model as doc_model

def simple_realize(sentences, char_limit):
	realized = ""
	first_sentence = True
	current = 0
	for s in sentences:
		sentence = s.full.replace("\n", " ")
		
		if not first_sentence:
			sentence = " " + sentence
		else:
			first_sentence = False
		
		current += len(sentence)
		if current > char_limit:
			break
		realized += sentence
	
	return realized
