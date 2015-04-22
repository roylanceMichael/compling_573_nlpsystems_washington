
wordLimit = 100

def simple_realize(sentences):
	realized = ""
	first_sentence = True
	current = 0
	for s in sentences:
		sentence = s.full.replace("\n", " ")

		if not first_sentence:
			sentence = "\n" + sentence
		else:
			first_sentence = False

		current += sentence.wordNum
		if current > wordLimit:
			break
		realized += sentence

	return realized
