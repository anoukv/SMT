
# Reads the viterbi parse from a file.
def read_vit(filename="viterbi.small"):
	f = open(filename,'r')
	lines = f.readlines()
	f.close()

	sentence_count = len(lines) / 3
	sentences = []
	for _ in xrange(sentence_count):
		# The first line is bs
		lines.pop(0)

		# For first line, create a map of 'index' => word
		firstline = filter(lambda x : not x == "", lines.pop(0).replace("\n","").split(" "))
		firstline = dict(zip(xrange(1,len(firstline)+1), firstline))

		# For second line, well, I didn't come up with the ridiculous string format, but this is how it can be read:
		secondline = map(lambda x : (x[0].replace(" ",""), map(int, filter(lambda x : not x == "", x[1].split(" ")))), filter(lambda x : len(x) == 2, map(lambda x : x.split("({"), lines.pop(0).replace("\n","").split("})"))))

		# Now loop over the sentences and combine them (something like a zip function)		
		pairs = []
		for (word, froms) in secondline:
			for index in froms:
				pairs.append((firstline[index], word))

		sentences.append(pairs)
	
	return sentences

# writes the translation table to the file "translations"
# for every f, it finds the most probable translation e
def writeTranslationTableToFile(t):
	file = open('translations', 'w')
	
	bestTrans = dict()
	for (f, e) in t:
		if f not in bestTrans:
			bestTrans[f] = (e, t[(f, e)])
		else:
			if t[(f, e)] > bestTrans[f][1]:
				bestTrans[f] = (e, t[(f, e)])

	for f in bestTrans:
		file.write(f + " " + bestTrans[f][0] +"\n")
	file.close()

# This just reads the corpus.
def loadData(f = "corpus.small.nl", e = "corpus.small.en"):
	fileo = open(f,'r')
	f = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	fileo = open(e,'r')
	e = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	[ x.append("NULL") for x in e ]
	fileo.close()

	return zip(f, e)