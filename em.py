from collections import defaultdict

def loadData(f = "corpus.small.nl", e = "corpus.small.en"):
	fileo = open(f,'r')
	f = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	fileo = open(e,'r')
	e = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	[ x.append("NULL") for x in e ]
	fileo.close()

	return zip(f, e)

def precision(referenceAlignments, ourAlignments):
	# we cannot really work with sets here, since they actually make sense
	# let's do this first
	return len(set(referenceAlignments).intersection(set(ourAlignments))) / float(len(ourAlignments))

def recall(referenceAlignments, ourAlignments):
	# again sets are not really allowed...
	# needs fixing
	return len(set(referenceAlignments).intersection(set(ourAlignments))) / float(len(referenceAlignments))

def initializeT(coprus):
	translationProbs = dict()
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] = 1
	return translationProbs

def initializeT_counted(coprus):
	translationProbs = defaultdict(int)
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] += 1
	return translationProbs

def maxViterbiAlignment(corpus, t):
	allAlignments = []
	for (f_s, e_s) in corpus:
		alignment = []
		for f in f_s:
			max = 0
			bestE = None
			for e in e_s:
				prob = t[(f, e)]
				if prob > max:
					max = prob
					bestE = e
			alignment.append((f, bestE))
		print alignment
		print
		allAlignments.append(alignment)
	return allAlignments

def em(corpus, init=initializeT):
	t = init(corpus)

	fe_set = set(t.keys())

	e_set = set()
	f_set = set()
	for (f, e) in corpus:
		for elem in e:
			e_set.add(elem)
		for elem in f:
			f_set.add(elem)

	for _ in xrange(10):
		count = dict( [(fe, 0) for fe in fe_set] )
		total = dict( [(e, 0) for e in e_set] )

		for (f_s, e_s) in corpus:
			total_s = dict( [ (f, 0) for f in f_s ] )

			for f in f_s:
				for e in e_s:
					total_s[f] += t[(f,e)]

			for f in f_s:
				total_s_f = float(total_s[f])
				for e in e_s:
					count[(f,e)] += t[(f,e)] / total_s_f
					total[e] += t[(f,e)] / total_s_f

		change = 0
		for (f, e) in fe_set:
			new = count[(f,e)] / total[e]
			change += abs(t[(f,e)] - new)
			t[(f,e)] = new
		# print "Change in this iteration:", change

	return t, change

if __name__ == "__main__":
	corpus = loadData()

	cute = False
	if cute:
		t = em(corpus)
		alignments = maxViterbiAlignment(corpus, t)
	else:
		t, change = em(corpus)
		print "Naive error:", change
		t, change = em(corpus, initializeT_counted)
		print "New error:", change


