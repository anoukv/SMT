from readers import read_datasets
# from plotter import plot_retreival
from collections import defaultdict
from math import sqrt
from time import time

def normalizeString(vec):
	vec = [ float(x) for x in vec]
	total = sqrt( sum([v**2 for v in vec]) )
	new_vec = []
	for v in vec:
		new_vec.append(v/total)
	return tuple(new_vec)

def load_vectors(filename, maxx=20000):
	print "\tLoading projections..."
	f = open(filename,'r')
	f.readline()
	content = [ filter( lambda x : not x in ["\n",""], l.replace("\n", "").split(" ")) for l in f.readlines() ]
	if len(content) > maxx:
		content = content[:maxx]
	content = [ (l[0], normalizeString(l[1:])) for l in content ]
	content = filter(lambda x : not x[1] == None, content)
	words = dict()
	for (word, vector) in content:
		words[word.lower()] = vector
	return words

def addToLimitSet(sett,word,score):
	sett.append((word,score))
	sett.sort(key=lambda tup: tup[1], reverse=True )
	sett.pop()

def findMostSimilarWords(vectors, word, top, cache):
	if word in cache:
		return cache[word]
	elif word in vectors:
		wordRepresentation = vectors[word]
		dim = len(wordRepresentation)
		mostSimilar = [(None, -1) for _ in xrange(top)]
		for wordvector in vectors:
			if wordvector != word:
				rep = vectors[wordvector]
				sim = sum([wordRepresentation[i] * rep[i] for i in xrange(dim)])
				addToLimitSet(mostSimilar, wordvector, sim)
		mostSimilar = tuple(map(lambda x: x[1], mostSimilar))
		cache[word] = mostSimilar
		return mostSimilar
	else:
		return []

def extendSentence(sentence, vectors, top, cache):
	extendedSentence = []
	for word in sentence:
		new = findMostSimilarWords(vectors, word, top, cache)
		extendedSentence.append(word)
		for extraWord in new:
			extendedSentence.append(extraWord)
	return extendedSentence

def get_counting_scores(vectorsEnglish, vectorsSpanish, verbose=True):
	cache = dict()
	def get_frequency_counts(train, vectorsEnglish, vectorsSpanish, cache):
		top = 3
		posW = defaultdict(int)
		negW = defaultdict(int)
		for (inset, sentence) in train:
			if inset:
				dic = posW
			else:
				dic = negW
			
			sentenceEn = extendSentence(sentence[0], vectorsEnglish, top, cache)
			sentenceEs = extendSentence(sentence[1], vectorsSpanish, top, cache)
			sentenceBoth = sentenceEn + sentenceEs
			for word in sentenceBoth:
				dic[word] += 1
		return (dict(posW), dict(negW))

	def score_sentences(mixed, (posW, negW), vectorsEnglish, vectorsSpanish, cache):
		results = []
		top = 5
		for (b, sentence) in mixed:
			net = 0
			
			sentenceEn = extendSentence(sentence[0], vectorsEnglish, top, cache)
			sentenceEs = extendSentence(sentence[1], vectorsSpanish, top, cache)
			
			sentenceBoth = sentenceEn + sentenceEs
			
			for word in sentenceBoth:
				if word not in posW and word not in negW:
					score = 0
				elif word in posW and word not in negW:
					score = 1
				elif word not in posW and word in negW:
					score = -1
				else:
					total = float(posW[word]+negW[word])
					score = 2 * (max(posW[word], negW[word]) / total - 0.5)
					if posW[word] < negW[word]:
						score = -score
				net += score
			results.append((b, net/float(len(sentence))))
		return sorted(results, key = lambda x : x[1], reverse=True)

	print "Loading data..."
	data = read_datasets(descriminative=True, development=True, flat=False)
	r = []
	for (mixed, train) in data:
		if verbose:
			print "\tTraining..."
		(posW, negW) = get_frequency_counts(train, vectorsEnglish, vectorsSpanish, cache)
		if verbose:
			print "\tScoring..."
		results = score_sentences(mixed, (posW, negW), vectorsEnglish, vectorsSpanish, cache)
		r.append(results)
		if verbose:
			print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
			print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
			print
	return tuple(r)

if __name__ == '__main__':
	start = time()
	pathEnglish = "../../project3_data/wordvectors.en"
	pathSpanish = "../../project3_data/wordvectors.es"

	vectorsEnglish = load_vectors(pathEnglish)
	vectorsSpanish = load_vectors(pathSpanish)

	results = get_counting_scores(vectorsEnglish, vectorsSpanish)

	stop = time()
	print "Time:", int(stop - start + 0.5)
	f = open('results_counting_scores_extended_3_200000.py', 'w')
	f.write("results = " + str(results))
	f.close()
	
	# plot_retreival(map(lambda x : x[0], results[0]))
	# plot_retreival(map(lambda x : x[0], results[1]))


