wordLimit = 100


def simple_realize(sentences):
	realized = ""
	first_sentence = True
	current = 0
	for s in sentences:
		sentence = " ".join(s.full.split())

		if not first_sentence:
			sentence = "\n" + sentence
		else:
			first_sentence = False

		current += s.wordNum
		if current > wordLimit:
			break
		realized += sentence

	return realized
