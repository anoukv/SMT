from pattern.en import tag as tagEN
from pattern.es import tag as tagES
import sklearn

from readers import read_datasets

from plotter import plot_retreival

from collections import defaultdict

def train(sentences):
	def get_index(tag, tag_dic):
		if not tag in tag_dic:
			tag_dic[tag] = len(tag_dic)
		return tag_dic[tag]

	new_sentences = []
	dic = dict()
	for (b, sent) in sentences:
		new_sentences.append((b, map(lambda x : get_index(x,dic), sent)))
	sentences = new_sentences

	dic_len = len(dic)
	X = []
	Y = []
	for (b, sent) in sentences:
		if b:
			X.append(1)
		else:
			X.append(0)

		weight = 1/float(len(sent))
		s = [ 0 for _ in xrange(dic_len)]
		for n in sent:
			s[n] += weight
		s.append(len(sent))
		Y.append(s)

	SVM = sklearn.svm.LinearSVC(tol=0.1)
	SVM.fit(X,Y)
	return SVM

def score_sentences(SVM, mixed):
	results = map(lambda x : (x[0], SVM.decision_function(x[1])), mixed)
	return sorted(results, key = lambda x : x[1], reverse=True)


def tag_sentence(sentence, tagger, app):
	try:
		return map(lambda x : x[1]+app, tagger("".join( [ x + " " for x in sentence ] )) )
	except:
		return [ str(len(sentence)) + app ]

def prepare_data(((mixed1, train1), (mixed2, train2))):
	sets = []
	for v in (mixed1, train1, mixed2, train2):
		vv = []
		for (b, (e,s)) in v:
			new = map(lambda x : tag_sentence(x, tagEN, "_en"), e) + map(lambda x : tag_sentence(x, tagES, "_es"), s)
			vv.append((b, new))
		sets.append(vv)

	return ((sets[0], sets[1]), (sets[2], sets[3]))

def meta_f_en(sentence):
	return map(lambda x : tag_sentence(x, tagEN, "_en"), sentence)

def meta_f_es(sentence):
	return map(lambda x : tag_sentence(x, tagEN, "_es"), sentence)

def go():
	print "Loading data..."
	# data = prepare_data(read_datasets(descriminative=True, development=True, flat=False))
	data = read_datasets(descriminative=True, development=True, flat=True, meta_f=(meta_f_en, meta_f_es))
	r = []
	for (mixed, train) in data:
		if verbose:
			print "\tTraining..."
		SVM = train(train)
		if verbose:
			print "\tScoring..."
		results = score_sentences(mixed, SVM)
		r.append(results)
		if verbose:
			print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
			print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
			print
	return tuple(r)



if __name__ == '__main__':
	results = go()
	plot_retreival(map(lambda x : x[0], results[0]))
	plot_retreival(map(lambda x : x[0], results[1]))


