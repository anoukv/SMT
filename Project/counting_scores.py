from readers import read_datasets

from plotter import plot_retreival

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
			net = 0
			for word in sentence:
				if word not in posW and word not in negW:
					score = 0
				elif word in posW and word not in negW:
					score = 1
				elif word not in posW and word in negW:
					score = -1
				else:
					total = float(posW[word]+negW[word])
					score = 2 * (max(posW[word], negW[word]) / total - 0.5)
					if posW[word] < negW[word]:
						score = -score
				net += score
			results.append((b, net/float(len(sentence))))
		return sorted(results, key = lambda x : x[1], reverse=True)

	print "Loading data..."
	data = read_datasets(descriminative=True, development=True, flat=True)
	r = []
	for (mixed, train) in data:
		if verbose:
			print "\tTraining..."
		(posW, negW) = get_frequency_counts(train)
		if verbose:
			print "\tScoring..."
		results = score_sentences(mixed, (posW, negW))
		r.append(results)
		if verbose:
			print "\tIn:", len(filter(lambda x:x[0], results[:50000]))
			print "\tOut:", len(filter(lambda x:x[0], results[50000:]))
			print
	return tuple(r)



if __name__ == '__main__':
	results = get_counting_scores()
	plot_retreival(map(lambda x : x[0], results[0]))
	plot_retreival(map(lambda x : x[0], results[1]))


