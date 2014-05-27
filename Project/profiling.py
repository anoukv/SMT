from readers import *
import nltk as nltk
from nltk.tag.simplify import simplify_wsj_tag
from time import time
import shelve

# converts frequency to relative frequency
def normalizeProfile(profile):
	# for every key
	for key in profile:
		# get the words and their counts
		counts = profile[key]
		# get the total count of words for this key
		total = float(sum(counts.values()))
		# divide every word by the total count to get relative frequency
		for key in counts:
			counts[key] = counts[key] / total
	return profile

# creates a relative frequency profile from a list of tagged sentences
def makeProfile(taggedSentences):
	profile = dict()
	# for every sentence and every tagged tuple in that sentence
	for sentence in taggedSentences:
		for taggedTuple in sentence:
			
			# get tag and word
			tag = taggedTuple[1]
			word = taggedTuple[0]

			# add the tag to the dictionary and increase its count

			# if the tag has been seen before
			if tag in profile:
				# get the countings dictionary
				counting = profile[tag]
				# if the word was seen before, increment
				if word in counting:
					counting[word] += 1
				# if not, set count to one
				else:
					counting[word] = 1
			# if the tag was not seen before, initialize the tag with a countings dictionary
			else:
				counting = dict()
				counting[word] = 1
				profile[tag] = counting
	return profile

# extracts the relative frequency profile from a corpus
def extractRelativeFrequencyProfile(corpus):
	
	# read the corpus, extract only the English sentences
	print "Reading corpus..."
	start = time()
	pairs = read_sentences(corpus, False)
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

	# create the profile
	print "Creating profile..."
	start = time()
	profile = makeProfile(sentences)
	stop = time()
	print "Creating profile took", int(stop-start+0.5), "seconds."
	
	# normalize the profile
	print "Normalizing profile..."
	start = time()
	profile = normalizeProfile(profile)
	stop = time()
	print "Normalizing profile took", int(stop-start+0.5), "seconds."

	# save the relative frequency profile to the profiles directory
	result = shelve.open("profiles/" + corpus + "_rf_profile")
	result.update(profile)
	result.close()

	return 1

# gets the difference profile between the domain and the general relative frequency profiles
def extractDifferenceProfile(domain, general):
	
	# get the specific relative frequency profiles
	domainProfile = shelve.open("profiles/" + domain + "_rf_profile")
	generalProfile = shelve.open("profiles/" + general + "_rf_profile")

	# initite empty dictionary for difference profile
	differenceProfile = dict()
	
	# check if the required files were created properly
	if len(domainProfile.keys()) == 0 or len(generalProfile.keys()) == 0:
		print "The required files were not yet created."
		return -1

	# for every tag in the domainProfile
	for tag in domainProfile:
		subDomainProfile = domainProfile[tag]
		differences = dict()
		
		# if the tag exists in the generalProfile
		if tag in generalProfile:
			
			# get the tag from the general profile
			subGeneralProfile = generalProfile[tag]
			
			# for every word in the tag of domainProfile
			for word in subDomainProfile:
				
				# if the word is in the tag of the generalProfile, get the difference domain-general
				if word in subGeneralProfile:
					differences[word] = subDomainProfile[word] - subGeneralProfile[word]
				
				# if the word is not in the general, set the difference to 1 (very specific to domain)
				else:
					differences[word] = 1
		
		# if the tag does not exist in the general profile, it is very unique
		# set everything to 1
		else:
			for word in subDomainProfile:
				differences[word] = 1

		# write differences for tag to differenceProfile
		differenceProfile[tag] = differences

	domainProfile.close()
	generalProfile.close()
	
	# save the result
	result = shelve.open("profiles/" + domain + "_difference_profile")
	result.update(differenceProfile)
	result.close()

	return 1

if __name__ == "__main__":
	
	# extract relative frequency profiles
	extractRelativeFrequencyProfile('software')
	extractRelativeFrequencyProfile('legal')
	extractRelativeFrequencyProfile('out')

	# extract difference profiles
	print "Extracting difference profile"
	start = time()
	extractDifferenceProfile('software', 'out')
	stop = time()
	print "Extracting difference profile took", int(stop-start+0.5), "seconds."

	print "Extracting difference profile"
	start = time()
	extractDifferenceProfile('legal', 'out')
	stop = time()
	print "Extracting difference profile took", int(stop-start+0.5), "seconds."

	