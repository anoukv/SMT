from readers import *
import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from collections import defaultdict

def prettyPrint(dictionary):
	for key in dictionary:
		print key, dictionary[key]

if __name__ == "__main__":
	pairsSoftware = read_sentences('software', False)
	pairsLegal = read_sentences('legal', False)
	software = [list(x[0]) for x in pairsSoftware]
	legal = [list(x[0]) for x in pairsLegal]
	software = software[0:5]
	legal = legal[0:5]
	software = [nltk.pos_tag(sen) for sen in software]
	legal = [nltk.pos_tag(sen) for sen in legal]
	#print software, legal

	profile = defaultdict(set)
	for sen in software:
		for tup in sen:
			profile[tup[1]].add(tup[0])

	prettyPrint(dict(profile))]


