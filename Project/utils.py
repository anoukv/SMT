from math import sqrt
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer 
wl = WordNetLemmatizer()

def normalize_vector(vec):
	total = sqrt( sum([v**2 for v in vec.values()]) )
	for key in vec.keys():
		vec[key] = vec[key] / total
	return vec

def vector_similarity(vec1, vec2):
	intersection = set(vec1.keys()).intersection(set(vec2.keys()))
	return sum([ vec1[elem] * vec2[elem] for elem in intersection ])

def vector_distance(vec1, vec2):
	return 1 - vector_similarity(vec1, vec2)

def hypernize_sentence(sentence):
	def hypernize(word):
		try:
			return wn.synsets(wl.lemmatize(word))[0].lexname.split(".")[1]
		except:
			return wl.lemmatize(word)
	return tuple(map(hypernize, sentence))
