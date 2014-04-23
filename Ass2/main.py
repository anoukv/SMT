from collections import defaultdict


def read_sentences_from_file(filename):
	f = open(filename, 'r')
	content = f.readlines()
	f.close()
	return filter(lambda x : not x len(x) == 0, map(lambda y : filter(lambda x : not x in [" ",""], y.replace("\n","").split(" ")), content))

def extract_phrases_from_sentence(sentence, length=4):
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

def extract_all_phrases(sentences):
	def add_phrases_to_dic(phrases, dic):
		for key, value in phrases.items():
			dic[key] += value

	phrases = defaultdict(int)
	for sentence in sentences:
		add_phrases_to_dic(extract_phrases_from_sentence(sentence), phrases)

	return phrases