from readers import *
import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from collections import defaultdict

def prettyPrint(dictionary):
	for key in dictionary:
		print key, dictionary[key]

def makeProfile(taggedSentences):
	profile = dict()
	for sentence in taggedSentences:
		for taggedTuple in sentence:
			tag = taggedTuple[1]
			word = taggedTuple[0]
			if tag in profile:
				counting = profile[tag]
				if word in counting:
					counting[word] += 1
				else:
					counting[word] = 1
			else:
				counting = dict()
				counting[word] = 1
				profile[tag] = counting
	return profile

if __name__ == "__main__":
	pairsSoftware = read_sentences('software', False)
	pairsLegal = read_sentences('legal', False)
	software = [list(x[0]) for x in pairsSoftware]
	legal = [list(x[0]) for x in pairsLegal]
	
	# for testing...
	software = software[0:5]
	legal = legal[0:5]
	
	# tag all sentences in the corpus
	software = [nltk.pos_tag(sen) for sen in software]
	legal = [nltk.pos_tag(sen) for sen in legal]


	prettyPrint(makeProfile(software))


