from collections import defaultdict


def read_sentences_from_file(filename):
	"""
		Reads sentences from file.
	"""
	f = open(filename, 'r')
	content = f.readlines()
	f.close()
	content = content.replace("\n","").split(" ")
	content = [ [ y for y in x if y not in ["", " "] ] for x in content ]
	return filter(lambda x : not len(x) == 0, content)

def extract_phrases_from_sentence(sentence, length=4):
	"""
		Reads grams from file and returns them in a dictionary with their counts.
	"""
	def add_gram_to_dic(gram, dic):
		for i in xrange(len(gram)):
			dic[tuple(gram[i:])] += 1

	phrases = defaultdict(int)
	gram = []
	while len(gram) < length and len(sentence) > 0:
		gram.append(sentence.pop(0))
		add_gram_to_dic(gram, phrases)

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
		for key, value in phrases.items():
			dic[key] += value
	def add_phrases_to_coc(pf, pe, dic):
		for (p1, p2) in [(pf,pe), (pe,pf)]:
			for key, value in p1.items():
				for p in p2.keys():
					dic[p][key] += value

	phrases_f = defaultdict(int)
	phrases_e = defaultdict(int)
	cocs = defaultdict(defaultdict)
	for (sentence_f, sentence_e) in sentences:
		p_f = extract_phrases_from_sentence(sentence_f)
		p_e = extract_phrases_from_sentence(sentence_e)

		add_phrases_to_dic(p_f, phrases_f)
		add_phrases_to_dic(p_e, phrases_e)
		add_phrases_to_coc(p_f, p_e, phrases_e)

	return (phrases_f, phrases_e, cocs)


	