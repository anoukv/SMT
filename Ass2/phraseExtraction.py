from collections import defaultdict
from time import time

from utils import *
from coverage import coverageSimple
from coverage_bf import coverage_bf

def extractAllPhrasesUpToLenght(sentence, n=4):
	phrases = set()
	for start in xrange(len(sentence)):
		for end in xrange(start, min(start+n, len(sentence))):
			phrases.add(tuple([i for i in xrange(start, end+1)]))
	return phrases #sorted(list(phrases), key = lambda x: x[0])

def getText(phrase, sentence):
	return tuple([sentence[i] for i in phrase])

def prettyPrint(phrasePairs, s_e, s_d):
	phrasePairs = sorted(phrasePairs, key = lambda x: x[0])
	for p in phrasePairs:
		print getText(p[0], s_e), getText(p[1], s_d)
	print
	return 0

def checkConsistency(phrases_e, phrases_d, alignmnent):
	phrasePairs = []
	inverseAlignment = invert_allignment(alignmnent)
	
	for phrase_e in phrases_e:
		for phrase_d in phrases_d:
			
			alignment_d = set()
			alignment_e = set()
			
			inAlignment_e = False
			inAlignment_d = False

			for word_e in phrase_e:
				if word_e in alignmnent:
					alignment_e = alignment_e.union(alignmnent[word_e])
					inAlignment_e = True

			if inAlignment_e:
				for word_d in phrase_d:
					if word_d in inverseAlignment:
						alignment_d = alignment_d.union(inverseAlignment[word_d])
						inAlignment_d = True

				if inAlignment_d and alignment_d.issubset(phrase_e) and alignment_e.issubset(phrase_d):
					phrasePairs.append((phrase_e, phrase_d))

	return phrasePairs

def P_e_given_f(e, f, cocs_f_e):
	if f in cocs_f_e and e in cocs_f_e[f]:
		freq_e_f = cocs_f_e[f][e]
		freq_total = sum( cocs_f_e[f].values() )
		return freq_e_f / float(freq_total)
	else:
		return 0

def P_f_given_e(f, e, cocs_e_f):
	return P_e_given_f(f, e, cocs_e_f)

def P_joint_e_f(e, f, phrases_f, cocs_f_e):
	if f in phrases_f:
		P_of_f = phrases_f[f] / float(sum( phrases_f.values() ))
		P_of_e_given_f = P_e_given_f(e, f, cocs_f_e)
		# print "Joining:", P_of_f, "*", P_of_e_given_f
		return P_of_f * P_of_e_given_f
	else:
		return 0

def generate_tables_from_sentences(triplets):
	def freqcrement(dic, phrases):
		for phrase in phrases:
			dic[phrase] += 1

	def coccrement(phrasePairs, dic, reverse=False):
		if reverse:
			phrasePairs = [ (x[1], x[0]) for x in phrasePairs ]
		for (phrase1, phrase2) in phrasePairs:
			if phrase1 not in dic:
				dic[phrase1] = defaultdict(int)
			dic[phrase1][phrase2] += 1

	(freqs_e, freqs_d) = (defaultdict(int), defaultdict(int))
	(cocs_e_f, cocs_f_e) = (dict(), dict())

	for (s_e, s_d, alignmnentDict) in triplets:
		phrases_e = extractAllPhrasesUpToLenght(s_e)
		phrases_d = extractAllPhrasesUpToLenght(s_d)

		freqcrement(freqs_e, [getText(x, s_e) for x in phrases_e])
		freqcrement(freqs_d, [getText(x, s_d) for x in phrases_d])

		phraseIndexes = checkConsistency(phrases_e, phrases_d, alignmnentDict)
		# prettyPrint(phraseIndexes, s_e, s_d)

		phrasePairs = [ (getText(x[0], s_e), getText(x[1], s_d)) for x in phraseIndexes ]
		coccrement(phrasePairs, cocs_e_f, False)
		coccrement(phrasePairs, cocs_f_e, True)

	return (freqs_e, freqs_d, cocs_e_f, cocs_f_e)

def expand_cocs(coc):
	expanded = dict()
	for key1 in coc:
		for key2 in coc[key1]:
			expanded[(key1,key2)] = coc[key1][key2]
	return expanded

if __name__ == "__main__":
	
	testMode = False
	get_coverage = False
	
	if testMode:
		s_d = ["michael", "geht", "davon", "aus", ",", "dass", "er", "im", "haus", "bleibt"]
		s_e = ["michael", "assumes", "that", "he", "will", "stay", "in", "the", "house"]
		alignmnent = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 5), (3, 6), (4, 9), (5, 9), (6, 7), (7, 7), (8, 8)]
		alignmnentDict = defaultdict(set)
		for (x, y) in alignmnent:
			alignmnentDict[x].add(y)
	else:
		print "Reading alignments..."
		alignmnentDicts = read_word_allignment_dicts("heldout/p2_heldout_symal.nlen")
		print "Reading sentences..."
		s_e = read_sentences_from_file("heldout/p2_heldout.nl")
		s_d = read_sentences_from_file("heldout/p2_heldout.en")
		print "Extracting..."

		if get_coverage:
			start = time()
			triplets = zip(s_e, s_d, alignmnentDicts)
			(_, _, cocs1, _) = generate_tables_from_sentences(triplets[:1])
			(_, _, cocs2, _) = generate_tables_from_sentences(triplets[1:2])
			# for i in xrange(10):
			# 	cocs2.pop(cocs2.keys()[0])
			cocs1 = expand_cocs(cocs1)
			cocs2 = expand_cocs(cocs2)
			stop = time()
			print coverageSimple(cocs2, cocs1)
			print coverage_bf(cocs2, cocs1)

		else:
			start = time()
			triplets = zip(s_e, s_d, alignmnentDicts)
			(freqs_e, freqs_d, cocs_e_f, cocs_f_e) = generate_tables_from_sentences(triplets)
			stop = time()
			print "Time:", int(stop-start), "seconds"
			for elem in (freqs_e, freqs_d, cocs_e_f, cocs_f_e):
				print len(elem)

			for i in xrange(0):
				(e, f) = (cocs_e_f.keys()[i], cocs_e_f[cocs_e_f.keys()[i]].keys()[0])
				print "\nPair:", (e, f)
				print "P(e|f) =", P_e_given_f(e, f, cocs_f_e)
				print "P(f|e) =", P_f_given_e(f, e, cocs_e_f)
				print "P(e,f) =", P_joint_e_f(e, f, freqs_d, cocs_f_e)

		




