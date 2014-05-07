from collections import defaultdict
from utils import *

def extractAllPhrasesUpToLenght(sentence, n=4):
	phrases = set()
	for start in xrange(len(sentence)):
		for end in xrange(start, min(start+n, len(sentence))):
			phrases.add(tuple([i for i in xrange(start, end+1)]))
	return sorted(list(phrases), key = lambda x: x[0])

def getText(phrase, sentence):
	return [sentence[i] for i in phrase]

def prettyPrint(phrasePairs, s_e, s_d):
	phrasePairs = sorted(phrasePairs, key = lambda x: x[0])
	for p in phrasePairs:
		print getText(p[0], s_e), getText(p[1], s_d)
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
			
			for word_d in phrase_d:
				if word_d in inverseAlignment:
					alignment_d = alignment_d.union(inverseAlignment[word_d])
					inAlignment_d = True


			if alignment_d.issubset(phrase_e) and alignment_e.issubset(phrase_d) and inAlignment_e and inAlignment_d:
				phrasePairs.append((phrase_e, phrase_d))

	return phrasePairs

if __name__ == "__main__":
	
	testMode = False
	
	if testMode:
		s_d = ["michael", "geht", "davon", "aus", ",", "dass", "er", "im", "haus", "bleibt"]
		s_e = ["michael", "assumes", "that", "he", "will", "stay", "in", "the", "house"]
		alignmnent = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 5), (3, 6), (4, 9), (5, 9), (6, 7), (7, 7), (8, 8)]
		alignmnentDict = defaultdict(set)
		for (x, y) in alignmnent:
			alignmnentDict[x].add(y)
	else:
		
		print "Reading alignments..."
		alignmnentDict = read_word_allignment_dicts("heldout/p2_heldout_symal.nlen")[5]
		print "Reading sentences..."
		s_e = read_sentences_from_file("heldout/p2_heldout.nl")[5]
		s_d = read_sentences_from_file("heldout/p2_heldout.en")[5]

	phrases_e = extractAllPhrasesUpToLenght(s_e)
	phrases_d = extractAllPhrasesUpToLenght(s_d)
	phrasePairs = checkConsistency(phrases_e, phrases_d, alignmnentDict)
	prettyPrint(phrasePairs, s_e, s_d)
