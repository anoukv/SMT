from utils import *

from collections import defaultdict


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
	gram = []
	# This loop is used to fill the gram
	while len(gram) < length and len(sentence) > 0:
		gram.append(sentence.pop(0))
		add_gram_to_dic(gram, phrases)

	# This loop is used to loop over the rest of the sentence when gram is already of max size.
	while len(sentence) > 0:
		gram.append(sentence.pop(0))
		gram.pop(0)
		add_gram_to_dic(gram, phrases)

	return phrases

def extract_all_phrases(sentence_pairs):
	"""
		Generates phrases for a collection of sentences.
	"""
	def add_phrases_to_dic(phrases, dic):
		# This function adds all items in phrases to dic
		for key, value in phrases.items():
			dic[key] += value
	def add_phrases_to_coc(p1, p2, dic):
		# This function adds for all p1 a count to p2.
		# This effectively registers all the cooccurence counts
		for key, value in p1.items():
			for p in p2.keys():
				if p not in dic:
					dic[p] = defaultdict(int)
				dic[p][key] += value

	phrases_f = defaultdict(int) # These are the french sentences
	phrases_e = defaultdict(int) # These are the english sentences

	cocs_e_to_f = dict() # This contains the cooccurences between phrase pairs.
	cocs_f_to_e = dict() # This contains the cooccurences between phrase pairs.

	for (sentence_f, sentence_e) in sentence_pairs:
		p_f = extract_phrases_from_sentence(sentence_f)
		p_e = extract_phrases_from_sentence(sentence_e)

		add_phrases_to_dic(p_f, phrases_f)
		add_phrases_to_dic(p_e, phrases_e)
		add_phrases_to_coc(p_f, p_e, cocs_f_to_e)
		add_phrases_to_coc(p_e, p_f, cocs_e_to_f)

	return (phrases_f, phrases_e, cocs_f_to_e, cocs_e_to_f)

if __name__ == "__main__":
	allignment = read_word_allignment_dicts()
	print allignment[0]
	assert False
	s_f = read_sentences_from_file("training/p2_training.nl")
	s_e = read_sentences_from_file("training/p2_training.en")
	pairs = zip(s_f, s_e)
	(phrases_f, phrases_e, cocs_f_to_e, cocs_e_to_f) = extract_all_phrases(pairs)
	print len(phrases_f), len(phrases_e), len(cocs)






