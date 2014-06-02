from readers import read_datasets

def save_results(results, filename="selected_sentences", data=None):
	print "Saving results.."

	filename = "../../project3_data/results/" + filename
	get_second = lambda x : [ y[1] for y in x ]

	results = (get_second(results[0]), get_second(results[1]))
	results = ([ x[0] for x in results[0]], [ x[0] for x in results[1]])
	if data==None:
		data = read_datasets(descriminative=True, development=True, flat=False)

	data = (get_second(data[0][0]), get_second(data[1][0]))

	for (scores, mixed) in zip(results, data):
		score_sentences = zip(scores, mixed)
		sentences = [ s[1] for s in sorted(score_sentences, key = lambda x : x[0], reverse=True)[:50000]]
		(english, spanish) = zip(*sentences)
		for (sentences, name) in zip((english, spanish), ( filename + ".en", filename + ".es")):
			f = open(name, 'w')
			for s in sentences:
				f.write("".join([word + " " for word in s]) + "\n")
			f.close()
