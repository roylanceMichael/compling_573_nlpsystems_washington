def perform(val1, val2):
	d = []
	for i in range(0, len(val1) + 1, 1):
		d.append([])
		for j in range(0, len(val2) + 1, 1):
			d[i].append(999)

	for i in range(0, len(val1) + 1, 1):
		for j in range(0, len(val2) + 1, 1):
			if i == 0 and j == 0:
				d[i][j] = 0

			if j == 0:
				d[i][j] = i
			elif i == 0:
				d[i][j] = j
			else:
				firstTemp = d[i - 1][j] + 1
				secondTemp = d[i][j - 1] + 1
				cost = 2
				if val1[i - 1] == val2[j - 1]:
					cost = 0

				thirdTemp = d[i - 1][j - 1] + cost

				if firstTemp <= secondTemp and firstTemp <= thirdTemp:
					d[i][j] = firstTemp
				elif secondTemp <= firstTemp and secondTemp <= thirdTemp:
					d[i][j] = secondTemp
				else:
					d[i][j] = thirdTemp

	return d[len(val1)][len(val2)]