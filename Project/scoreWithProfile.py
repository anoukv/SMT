from readers import *
import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from time import time
import shelve

def scoreSentences(sentences, differences):
	
	scoredSentences = []
	for sen in sentences:	
		score = 0
		for word, tag in sen:
			if tag in differences:
				counting = differences[tag]
				if word in counting:
					score += counting[word]

		# if the score is smaller than 0, readjust to zero
		if score <= 0:
			score = 0
		
		# otherwise, normalize
		else:
			score = score / float(len(sen))

		# add tuple score, taggedSentence to scoredSentences
		scoredSentences.append((score, sen))
	return scoredSentences

def getTaggedCorpus(corpus):
	# read the corpus, extract only the English sentences
	start = time()
	pairs = read_sentences(corpus, False)
	pairs = pairs[1:5]
	sents = [list(x[0]) for x in pairs]
	stop = time()
	print "Reading corpus took", int(stop-start+0.5), "seconds."

	print "Tagging corpus..."
	start = time()
	
	sentences = []
	# for every sentence
	for sen in sents:
		# tag the sentence with nltk pos tagger
		tagged = nltk.pos_tag(sen)
		# simplify the tagging to simplified POS-tags (see http://www.nltk.org/book/ch05.html)
		simplified = [(word,  simplify_wsj_tag(tag)) for word, tag in tagged]
		# append the simplified tagged sentence to sentences
		sentences.append(simplified)

	stop = time()
	print "Tagging corpus took", int(stop-start+0.5), "seconds."
	return sentences

if __name__ == "__main__":
	domain = 'software'
	differences = shelve.open("profiles/" + domain + "_difference_profile")
	((mixedLegal, legal), (mixedSoftware, software)) = read_datasets()
	print mixedSoftware[1]
	#corpus = getTaggedCorpus(mixedSoftware)
	#scoredSentences = scoreSentences(corpus, differences)
	
	