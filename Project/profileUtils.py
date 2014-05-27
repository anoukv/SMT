import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from time import time

def getTaggedEnglishCorpus(corpus):
	corpus = corpus[1:500]
	sents = [list(x[1][0]) for x in corpus]
	
	print "Tagging corpus..."
	start = time()
	
	taggedSentences = []
	# for every sentence
	for sen in sents:
		# tag the sentence with nltk pos tagger
		tagged = nltk.pos_tag(sen)
		# simplify the tagging to simplified POS-tags (see http://www.nltk.org/book/ch05.html)
		simplified = [(word,  simplify_wsj_tag(tag)) for word, tag in tagged]
		# append the simplified tagged sentence to sentences
		taggedSentences.append(simplified)
	
	stop = time()
	print "Tagging corpus took", int(stop-start+0.5), "seconds."
	
	return taggedSentences