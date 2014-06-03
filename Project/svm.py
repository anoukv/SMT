from pattern.en import tag as tagEN
from pattern.es import tag as tagES
from sklearn import svm as sk_svm

from readers import read_datasets

from plotter import plot_r
from results_to_files import save_results

from collections import defaultdict

def data_to_svm_input(data):
	print "\t\tConverting sentences to vectors..."
	dic = dict()
	def get_index(tag, tag_dic):
		if not tag in tag_dic:
			tag_dic[tag] = len(tag_dic)
		return tag_dic[tag]

	# Get a number for every postag
	new_data = []
	for pair in data:
		mt = []
		for sentences in pair:
			new_sentences = []
			for (b, sent) in sentences:
				new_sentences.append((b, map(lambda x : get_index(x, dic), sent)))
			mt.append(new_sentences)
		new_data.append(tuple(mt))

	data = tuple(new_data)
	dic_len = len(dic)

	# Get a vector for every sentence and split boolean and vector
	new_data = []
	for pair in data:
		mt = []
		for sentences in pair:
			X = []
			y = []
			for (b, sent) in sentences:
				if b:
					y.append(1)
				else:
					y.append(0)
				s = [ 0 for _ in xrange(dic_len)]
				for n in sent:
					s[n] += 1
				X.append(s)
			mt.append((X,y))
		new_data.append(tuple(mt))

	return tuple(new_data)

def train_svm((X,y)):
	print "\t\tFinding support vectors..."
	SVM = sk_svm.LinearSVC(tol=0.001)
	# SVM = sk_svm.SVC(kernel='poly')
	SVM.fit(X,y)
	return SVM

def score_sentences((X,y), SVM):
	results = []
	for (b,s) in zip(y,X):
		results.append((b,SVM.decision_function(s)))
	return results, sorted(results, key = lambda x : x[1], reverse=True)

def go():
	print "Loading data..."
	original_data = read_datasets(descriminative=True, development=True, flat=True, ext=".pos")
	data = data_to_svm_input(original_data)
	r = []
	o = []
	for (mixed, train) in data:
		print "\tTraining..."
		SVM = train_svm(train)
		print "\tScoring..."
		original, results = score_sentences(mixed, SVM)
		r.append(results)
		o.append(original)
		print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
		print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
		print
	return o, tuple(r)



if __name__ == '__main__':
	original, results = go()
	save_results(original, filename="svm_results")
	plot_r(results)


