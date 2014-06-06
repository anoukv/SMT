from utils import normalize_vector

from collections import defaultdict

def sentences_pairs_as_word_features(sentences):
	pairs = []
	index_dic_l = dict()
	index_dic_r = dict()
	for (left, right) in sentences:
		l = sentences_as_word_features(left, index_dic_l)
		r = sentences_as_word_features(right, index_dic_r)
		pairs.append((l,r))
	return pairs

def sentence_vector(sentence):
	def get_index(dic, word):
		if not word in dic:
			dic[word] = len(dic)
		return dic[word]
	feature_vec = defaultdict(int)
	for word in sentence:
		feature_vec[word] += 1
	return dict(normalize_vector(feature_vec))

def sentence_as_feature(sentence, index_dic):
	def get_index(dic, word):
		if not word in dic:
			dic[word] = len(dic)
		return dic[word]
	feature_vec = defaultdict(int)
	for word in sentence:
		feature_vec[get_index(index_dic, word)] += 1
	return dict(normalize_vector(feature_vec))

def sentences_flat_as_word_features(sentences):
	index_dic = dict()
	sentence_features = []
	for sentence in sentences:
		s = sentence_as_feature(sentence, index_dic)
		sentence_features.append(s)
	return sentence_features

 