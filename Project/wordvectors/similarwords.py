from collections import defaultdict
from math import sqrt

def normalizeString(vec):
	vec = [ float(x) for x in vec]
	total = sqrt( sum([v**2 for v in vec]) )
	new_vec = []
	for v in vec:
		new_vec.append(v/total)
	return tuple(new_vec)

def load_vectors(filename):
	print "Loading word projections"
	f = open(filename,'r')
	f.readline()
	content = [ filter( lambda x : not x in ["\n",""], l.replace("\n", "").split(" ")) for l in f.readlines() ]
	content = [ (l[0], normalizeString(l[1:])) for l in content ]
	content = filter(lambda x : not x[1] == None, content)
	words = dict()
	for (word, vector) in content:
		words[word.lower()] = vector

	print "Done!"
	return words

def findMostSimilarWords(vectors, word, top):
	
	wordRepresentation = vectors[word]
	dim = len(wordRepresentation)
	
	mostSimilar = [(0, None) for i in xrange(top)]
	
	for wordvector in vectors:
		if wordvector != word:
			rep = vectors[wordvector]
			sim = sum([wordRepresentation[i] * rep[i] for i in xrange(dim)])
			filled = False
			
			for i in xrange(top):
				if (sim > mostSimilar[i][0] or mostSimilar == None) and filled == False:
					for j in xrange(top):
						index = top - 1 -j
						if index > i:
							mostSimilar[index] = mostSimilar[index-1]
					mostSimilar[i] = (sim, wordvector)
					filled = True
	
	return mostSimilar

if __name__ == "__main__":
	v = load_vectors('/Users/anoukvisser/dev/Python/project3_data/wordvectors.en')
	print findMostSimilarWords(v, "software", 10)

