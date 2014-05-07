from collections import defaultdict
from utils import *

def extractAllPhrasesUpToLenght(sentence, n=4):
	phrases = set()
	for start in xrange(len(sentence)):
		for end in xrange(start, min(start+4, len(sentence)-1)):
			phrase = [i for i in xrange(start, end+1)]
			phrases.add(tuple(phrase))
	return phrases

def getText(phrase, sentence):
	return [sentence[i] for i in phrase]

def prettyPrint(phrasePairs):
	for p in phrasePairs:
		print p
	return 0

def checkConsistency(phrases_e, phrases_d, alignmnent, s_e, s_d):
	
	phrasePairs = []
	inverseAlignment = invert_allignment(alignmnent)
	print alignmnent 
	print inverseAlignment
	
	# check all combinations
	for e, phrase_e in enumerate(phrases_e):
		for d, phrase_d in enumerate(phrases_d):
			happy = False
			
			if len(set(phrase_e).intersection(set(alignmnent.keys()))) > 0:

				# for every word in the e phrase, check if there exists an a containing 
				# the word that also contains a word from f
				for word_e in phrase_e:
					a1 = alignmnent[word_e]
					if len(set(phrase_d).intersection(a1)) > 0:

						# then, check for every word in the f phrase if there exists an a containing 
						# the word that also contains a word from e
						for word_d in phrase_d:
							a2 = set()
							
							if word_d in inverseAlignment:
								a2 = inverseAlignment[word_d]
							
							if len(set(phrase_e).intersection(a2)) > 0:
								phrasePairs.append((getText(phrase_e, s_e), getText(phrase_d, s_d)))
								 

	return phrasePairs

if __name__ == "__main__":
	s_d = ["michael", "geht", "davon", "aus", ",", "dass", "er", "im", "haus", "bleibt"]
	s_e = ["michael", "assumes", "that", "he", "will", "stay", "in", "the", "house"]
	alignmnent = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 5), (3, 6), (4, 9), (5, 9), (6, 7), (7, 7), (8, 8)]

	alignmnentDict = defaultdict(set)
	for (x, y) in alignmnent:
		alignmnentDict[x].add(y)

	phrases_e = extractAllPhrasesUpToLenght(s_e)
	phrases_d = extractAllPhrasesUpToLenght(s_d)
	checkConsistency(phrases_e, phrases_d, alignmnentDict, s_e, s_d)
