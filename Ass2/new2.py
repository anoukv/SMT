from collections import defaultdict
from utils import *

def extractAllPhrasesUpToLenght(sentence, n=20):
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

def hasAlignmentInPhrase(word, phrase, alignmnent):
	return len(alignmnent[word].intersection(set(phrase))) > 0


def checkConsistency(phrases_e, phrases_d, alignmnent, s_e, s_d):
	phrasePairs = []
	inverseAlignment = invert_allignment(alignmnent)
	print alignmnent
	print inverseAlignment

	for phrase_e in phrases_e:
		for phrase_d in phrases_d:
			
			alignment_d = set()
			alignment_e = set()
			

			for word_e in phrase_e:
				if word_e in alignmnent:
					alignment_e = alignment_e.union(alignmnent[word_e])
			
			for word_d in phrase_d:
				if word_d in inverseAlignment:
					alignment_d = alignment_d.union(inverseAlignment[word_d])

			if len(phrase_e) > 7:
				print getText(phrase_e, s_e)
				print getText(phrase_d, s_d)
				print "Aligned to d", alignment_e, "(d)", phrase_d
				print "Aligned to e", alignment_d, "(e)", phrase_e
				print

			if alignment_d.issubset(phrase_e) and alignment_e.issubset(phrase_d):
				phrasePairs.append((phrase_e, phrase_d))
				# print "\n\n ------------- \n\n"
				# print "Considering..."
				# print getText(phrase_e, s_e)
				# print getText(phrase_d, s_d)
				# print "Aligned to d", alignment_e, "(d)", phrase_d
				# print "Aligned to e", alignment_d, "(e)", phrase_e
				# for word_d in phrase_d:
				# 	print word_d
				# 	if word_d in inverseAlignment:
				# 		print inverseAlignment[word_d]

				

	
	return phrasePairs

if __name__ == "__main__":
	testMode = True
	if testMode:
		s_d = ["michael", "geht", "davon", "aus", ",", "dass", "er", "im", "haus", "bleibt"]
		s_e = ["michael", "assumes", "that", "he", "will", "stay", "in", "the", "house"]
		alignmnent = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 5), (3, 6), (4, 9), (5, 9), (6, 7), (7, 7), (8, 8)]

		alignmnentDict = defaultdict(set)
		for (x, y) in alignmnent:
			alignmnentDict[x].add(y)

	phrases_e = extractAllPhrasesUpToLenght(s_e)
	phrases_d = extractAllPhrasesUpToLenght(s_d)

	print phrases_e
	print phrases_d

	phrasePairs = checkConsistency(phrases_e, phrases_d, alignmnentDict, s_e, s_d)
	print 
	print
	prettyPrint(phrasePairs, s_e, s_d)
