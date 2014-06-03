from readers import read_datasets

# from plotter import plot_r
from results_to_files import save_results

from collections import defaultdict

def get_counting_scores(verbose=True):
	def get_frequency_counts(train):
		posW = defaultdict(int)
		negW = defaultdict(int)
		for (inset, sentence) in train:
			if inset:
				dic = posW
			else:
				dic = negW
			for word in sentence:
				dic[word] += 1
		return (dict(posW), dict(negW))

	def score_sentences(mixed, (posW, negW)):
		results = []
		for (b, sentence) in mixed:
			pos = 0
			for word in sentence:
				if word not in posW and word not in negW:
					score = 0.5
				elif word in posW and word not in negW:
					score = 1
				elif word not in posW and word in negW:
					score = 0
				else:
					score = posW[word] / float(posW[word]+negW[word])
					
				pos += score
			results.append((b, pos/float(len(sentence)+2)))

		return results, sorted(results, key = lambda x : x[1], reverse=True)

	print "Loading data..."
	data = read_datasets(descriminative=True, development=True, flat=True, ext="")
	r = []
	o = []
	for (mixed, train) in data:
		if verbose:
			print "\tTraining..."
		(posW, negW) = get_frequency_counts(train)
		if verbose:
			print "\tScoring..."
		original, results = score_sentences(mixed, (posW, negW))
		r.append(results)
		o.append(original)
		if verbose:
			print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
			print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
			print
	return o, tuple(r)



if __name__ == '__main__':
	original, results = get_counting_scores()
	save_results(original, filename="wbs_results")
	# plot_r(results)


