from utils import *

from collections import defaultdict
from time import time

def extract_phrases_from_sentence(sentence, length=4):
	"""
		Reads grams from file and returns them in a dictionary with their counts.
		The function loops over the sentence and maintains a gram of the length last words.
		Each time a word is added to the gram the state of the gram is used to increment the dictionary.
	"""
	def add_gram_to_dic(gram, dic):
		# This function adds all appropriate sub-grams to the dictionary.
		for i in xrange(len(gram)):
			dic[tuple(gram[i:])] += 1

	phrases = defaultdict(int)
	index = 1
	gram = []

	# This loop is used to build and store the grams.
	while len(sentence) > 0:
		gram.append((index, sentence.pop(0)))
		if len(gram) > length: # if gram is over filled
			gram.pop(0)
		add_gram_to_dic(gram, phrases)
		index += 1
	return phrases

def get_valid_phrase_pairs(p_e, p_f, allignment):
	""" 
		Checks all combinations of p_e and p_f elements for being valid sub-phrases.
		Function starts with many private declarations. Then computes in double for loop.
	"""
	def allignment_is_bidirectional(p_e, p_f, allignment, inv_allignment):
		""" 
			Asserts an allignment is bidirectional.
			This checks the first two conditions in Koehn Chapter 5.2.2 eq. 5.3
		"""
		# For each direction
		for (p1, p2, a) in ((p_e, p_f, allignment), (p_f, p_e, inv_allignment)):
			# For every word number in sequence1
			for n in p1:
				# If it has an allignment
				if n in a:
					# For every word number in its' alignment
					for e in a[n]:
						# That word has to be in the opposing sentence
						if not e in p2:
							return False
		# Did not find violations.
		return True

	def set_has_member(s1, s2):
		""" 
			Asserts that at least one element in s1 is in s2.
			This checks the third condition in Koehn Chapter 5.2.2 eq. 5.3 
		"""
		for elem in s1:
			if elem in s2:
				return True
		return False

	get_index_list = lambda x : set([ y[0] for y in x ])
	get_words_tuple = lambda x : tuple([ y[1] for y in x ])
	
	inv_allignment = invert_allignment(allignment)

	# For every possible pair (e,f) check if the conditions hold that:
	# 	alligned_has_no_interupts AND allignment_is_bidirectional
	pairs = []
	for e in p_e:
		e_indexes = get_index_list(e)
		if set_has_member(e_indexes, allignment.keys()):
			for f in p_f:
				if allignment_is_bidirectional(e_indexes, get_index_list(f), allignment, inv_allignment):
					pairs.append((get_words_tuple(e), get_words_tuple(f)))
	
	return pairs

def extract_all_phrases(sentence_pairs):
	"""
		Generates phrases for a collection of sentences.
	"""
	def add_phrases_to_dic(phrases, dic):
		# This function adds all items in phrases to dic
		for key in phrases:
			dic[key] += 1

	def add_phrases_to_coc(pairs, dic):
		# This function adds for all p1 a count to p2.
		# This effectively registers all the cooccurence counts
		for (e,f) in pairs:
			if e not in dic:
				dic[e] = defaultdict(int)
			dic[e][f] += 1
		
	phrases_f = defaultdict(int) # These are the french sentences
	phrases_e = defaultdict(int) # These are the english sentences

	cocs = dict() # This contains the cooccurences between phrase pairs.

	for (sentence_f, sentence_e, allignment) in sentence_pairs:
		p_f = extract_phrases_from_sentence(sentence_f)
		p_e = extract_phrases_from_sentence(sentence_e)

		pairs = get_valid_phrase_pairs(p_e, p_f, allignment)
		phrase_e = [ p[0] for p in pairs ]
		phrase_f = [ p[1] for p in pairs ]

		add_phrases_to_dic(phrase_e, phrases_e)
		add_phrases_to_dic(phrase_f, phrases_f)
		add_phrases_to_coc(pairs, cocs)
	
	return (phrases_e, phrases_f, cocs)

def debug():
	s_e = [['tot', 'slot', 'is', 'er', 'nog', 'het', 'gebrek', 'aan', 'transparantie', '.']]
	s_f = [['finally', ',', 'there', 'is', 'the', 'lack', 'of', 'transparency', '.']]
	allignment = [dict({0: set([0]), 1: set([0, 1]), 2: set([3]), 3: set([2]), 5: set([4]), 6: set([5, 6]), 7: set([5]), 8: set([7]), 9: set([8])})]

	(phrases_e, phrases_f, cocs) = extract_all_phrases(zip(s_f, s_e, allignment))
	for e in (phrases_e, phrases_f, cocs):
		print len(e)

	assert False, "Debug ends here"

if __name__ == "__main__":
	print "Reading data..."
	allignment = read_word_allignment_dicts()
	s_f = read_sentences_from_file("training/p2_training.nl")
	s_e = read_sentences_from_file("training/p2_training.en")
	print "Extracting phrases..."
	start = time()
	pairs = zip(s_f, s_e, allignment)
	(phrases_e, phrases_f, cocs) = extract_all_phrases(pairs)
	stop = time()
	print "Time: ", int(stop - start + 0.5), "seconds"
	print len(phrases_f), len(phrases_e), len(cocs), len(pairs)






