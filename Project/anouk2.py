from readers import *
import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from collections import defaultdict
from time import time
import shelve

def prettyPrint(dictionary):
	for key in dictionary:
		print key, dictionary[key]

def normalizeProfile(profile):
	
	for key in profile:
		counts = profile[key]
		total = float(sum(counts.values()))
		for key in counts:
			counts[key] = counts[key] / total
	
	return profile

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

def extractRelativeFrequencyProfile(corpus):
	
	print "Reading corpus..."
	start = time()
	pairs = read_sentences(corpus, False)
	pairs = pairs[:500]
	sentences = [list(x[0]) for x in pairs]
	stop = time()
	print "Reading corpus took", int(stop-start+0.5), "seconds."
	
	print "Tagging corpus..."
	start = time()
	sentences = [nltk.pos_tag(sen) for sen in sentences]
	stop = time()
	print "Tagging corpus took", int(stop-start+0.5), "seconds."

	print "Creating profile..."
	start = time()
	profile = makeProfile(sentences)
	stop = time()
	print "Creating profile took", int(stop-start+0.5), "seconds."
	
	print "Normalizing profile..."
	start = time()
	profile = normalizeProfile(profile)
	stop = time()
	print "Normalizing profile took", int(stop-start+0.5), "seconds."

	result = shelve.open(corpus + "_rf_profile")
	result.update(profile)
	result.close()

	return 1

if __name__ == "__main__":
	extractRelativeFrequencyProfile('software')
	extractRelativeFrequencyProfile('legal')
	


	# prettyPrint(profile)



