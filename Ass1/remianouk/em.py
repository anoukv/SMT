from collections import defaultdict

from util import *

# computes the average precision or recall (specified by method)
# over all sentences
def average_sentence_score(referenceAlignments, ourAlignments, method):
	return sum(map(lambda x : method(x[0], x[1]), zip(referenceAlignments, ourAlignments))) / float(len(referenceAlignments))

# Counts every item in a list, returns as a dictionary.
def transform_to_counted_dict(list_set):
	total = defaultdict(int)
	for elem in list_set:
		total[elem] += 1
	return total

# Calculates alignment precision
def precision(referenceAlignments, ourAlignments):
	refset = set(referenceAlignments)
	ourset = set(ourAlignments)
	intersect = refset.intersection(ourset)

	counted_ref = transform_to_counted_dict(referenceAlignments)
	counted_our = transform_to_counted_dict(ourAlignments)

	total_good = 0
	for e in intersect:
		total_good += counted_our[e] 
		if counted_our[e] > counted_ref[e]:
			total_good -= counted_our[e] - counted_ref[e]

	return  total_good / float(len(ourAlignments))

# Initializes the translation table uniformly
# in this case we'll just set every possible alignment
# (e, j) to 1
def initializeT(coprus):
	translationProbs = dict()
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] = 1
	return translationProbs

# initializatoin based on frequency and length similarity
def initializeT_counted_lensim(coprus):
	def word_similarity_score(word1, word2):
		if len(word1) > len(word2):
			tmp = word1
			word1 = word2
			word2 = tmp
		return 1 + len(word1) / float(len(word2))

	translationProbs = defaultdict(int)
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] += word_similarity_score(f,e)
	return translationProbs

# improvmenet over uniform initializatoin
def initializeT_counted(coprus):
	translationProbs = defaultdict(int)
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] += 1
	return translationProbs

# Outputs the viterbi alignments, by matching f, with the 
# e that has the highest probability. We can do this using
# only the translation table because we are working with a
# word-based model, so the viterbi alignment equals the translations
# that have the highest probabilities.
def maxViterbiAlignment(corpus, t):
	allAlignments = []
	for (f_s, e_s) in corpus:
		alignment = []
		for f in f_s:
			max = 0
			bestE = None
			for e in e_s:
				prob = t[(f, e)]
				if prob > max:
					max = prob
					bestE = e
			alignment.append((f, bestE))
		allAlignments.append(alignment)
	return allAlignments

# the EM algorithm for IBM Model 1
def em(corpus, iterations=10, init=initializeT_counted):
	t = init(corpus)

	fe_set = set(t.keys())

	e_set = set()
	f_set = set()
	for (f, e) in corpus:
		for elem in e:
			e_set.add(elem)
		for elem in f:
			f_set.add(elem)

	for _ in xrange(iterations):
		count = dict( [(fe, 0) for fe in fe_set] )
		total = dict( [(e, 0) for e in e_set] )

		for (f_s, e_s) in corpus:
			total_s = dict( [ (f, 0) for f in f_s ] )

			for f in f_s:
				for e in e_s:
					total_s[f] += t[(f,e)]

			for f in f_s:
				total_s_f = float(total_s[f])
				for e in e_s:
					count[(f,e)] += t[(f,e)] / total_s_f
					total[e] += t[(f,e)] / total_s_f

		change = 0
		for (f, e) in fe_set:
			new = count[(f,e)] / total[e]
			change += abs(t[(f,e)] - new)
			t[(f,e)] = new
		# print "Change in this iteration:", change

	return t, change

if __name__ == "__main__":
	from time import time
	start = time()
	corpus = loadData()
	baseline = read_vit()

	iterations = 20
	
	t, change = em(corpus, iterations, initializeT_counted_lensim)
	alignments = maxViterbiAlignment(corpus, t)
	p = average_sentence_score(baseline, alignments, precision)
	print "P:", p

	t, change = em(corpus, iterations, initializeT)
	alignments = maxViterbiAlignment(corpus, t)
	p = average_sentence_score(baseline, alignments, precision)
	print "P:", p

	t, change = em(corpus, iterations, initializeT_counted)
	alignments = maxViterbiAlignment(corpus, t)
	p = average_sentence_score(baseline, alignments, precision)
	print "P:", p

	writeTranslationTableToFile(t)
	stop = time()
	print "Time spend:", int(stop - start + 0.5), "seconds"


