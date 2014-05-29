from readers import read_datasets
from plotter import plot_retreival
from collections import defaultdict
from math import sqrt
import sys

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

def findMostSimilarWords(vectors, word, top=10):
	if word in vectors:
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
		return map(lambda x: x[1], mostSimilar)
	else:
		return []

def extendSentence(sentence, vectors, top):
	print sentence
	extendedSentence = []
	for word in sentence:
		new = findMostSimilarWords(vectors, word, top)
		extendedSentence.append(word)
		for extraWord in new:
			extendedSentence.append(extraWord)
	print extendedSentence
	return extendedSentence

def get_counting_scores(vectorsEnglish, vectorsSpanish, verbose=True):
	def get_frequency_counts(train, vectorsEnglish, vectorsSpanish):
		top = 5
		posW = defaultdict(int)
		negW = defaultdict(int)
		for (inset, sentence) in train:
			if inset:
				dic = posW
			else:
				dic = negW
			
			sentenceEn = extendSentence(sentence[0], vectorsEnglish, top)
			sentenceEs = extendSentence(sentence[1], vectorsSpanish, top)
			sentenceBoth = sentenceEn + sentenceEs
			for word in sentenceBoth:
				dic[word] += 1
		return (dict(posW), dict(negW))

	def score_sentences(mixed, (posW, negW), vectorsEnglish, vectorsSpanish):
		results = []
		top = 5
		for (b, sentence) in mixed:
			net = 0
			
			sentenceEn = extendSentence(sentence[0], vectorsEnglish, top)
			sentenceEs = extendSentence(sentence[1], vectorsSpanish, top)
			
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
		(posW, negW) = get_frequency_counts(train, vectorsEnglish, vectorsSpanish)
		if verbose:
			print "\tScoring..."
		results = score_sentences(mixed, (posW, negW), vectorsEnglish, vectorsSpanish)
		r.append(results)
		if verbose:
			print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
			print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
			print
	return tuple(r)



if __name__ == '__main__':
	if not len(sys.argv) == 3:
		print "USAGE: "
		print "python counting_scores_extended.py <PATH TO WORDVECOTRS_EN> <PATH TO WORDVECOTRS_ES>"
		sys.exit()
	else:

		pathEnglish = sys.argv[1]
		pathSpanish = sys.argv[2]

		vectorsEnglish = load_vectors(pathEnglish)
		vectorsSpanish = load_vectors(pathSpanish)
		
		results = get_counting_scores(vectorsEnglish, vectorsSpanish)
		
		plot_retreival(map(lambda x : x[0], results[0]))
		plot_retreival(map(lambda x : x[0], results[1]))


