from collections import defaultdict

from util import read_vit

def loadData(f = "corpus.small.nl", e = "corpus.small.en"):
	fileo = open(f,'r')
	f = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	fileo = open(e,'r')
	e = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	[ x.append("NULL") for x in e ]
	fileo.close()

	return zip(f, e)

def average_sentence_score(referenceAlignments, ourAlignments, method):
	return sum(map(lambda x : method(x[0], x[1]), zip(referenceAlignments, ourAlignments))) / float(len(referenceAlignments))

def transform_to_counted_dict(list_set):
	total = defaultdict(int)
	for elem in list_set:
		total[elem] += 1
	return total

def precision(referenceAlignments, ourAlignments):
	refset = set(referenceAlignments)
	ourset = set(ourAlignments)
	intersect = refset.intersection(ourset)

	counted_ref = transform_to_counted_dict(referenceAlignments)
	counted_our = transform_to_counted_dict(ourAlignments)

	total_good = 0
	for e in intersect:
		total_good += counted_our[e] 
		if counted_our[e] > counted_ref[e]:
			total_good -= counted_our[e] - counted_ref[e]

	return  total_good / float(len(ourAlignments))

def recall(referenceAlignments, ourAlignments):
	refset = set(referenceAlignments)
	ourset = set(ourAlignments)
	intersect = refset.intersection(ourset)

	counted_ref = transform_to_counted_dict(referenceAlignments)
	counted_our = transform_to_counted_dict(ourAlignments)

	total_good = 0
	for e in intersect:
		total_good += counted_our[e] 
		if counted_our[e] > counted_ref[e]:
			total_good -= counted_our[e] - counted_ref[e]

	return  total_good / float(len(referenceAlignments))

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

def writeTranslationTableToFile(t):
	file = open('translations', 'w')
	
	bestTrans = dict()
	for (f, e) in t:
		if f not in bestTrans:
			bestTrans[f] = (e, t[(f, e)])
		else:
			if t[(f, e)] > bestTrans[f][1]:
				bestTrans[f] = (e, t[(f, e)])

	for f in bestTrans:
		print f, bestTrans[f][0]
		file.write(f + " " + bestTrans[f][0] +"\n")
	file.close()

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
		allAlignments.append(alignment)
	return allAlignments

def em(corpus, iterations=10, init=initializeT_counted):
	t = init(corpus)

	fe_set = set(t.keys())

	e_set = set()
	f_set = set()
	for (f, e) in corpus:
		for elem in e:
			e_set.add(elem)
		for elem in f:
			f_set.add(elem)

	for _ in xrange(iterations):
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
	from time import time
	start = time()
	print "Loading corpus..."
	corpus = loadData()

	iterations = 20
	t, change = em(corpus, iterations, initializeT)
	print "Table error:", change

	alignments = maxViterbiAlignment(corpus, t)
	baseline = read_vit()

	p = average_sentence_score(baseline, alignments, precision)
	r = average_sentence_score(baseline, alignments, recall) 

	print "P:", p, "R:", r

	t, change = em(corpus, iterations)
	print "Table error:", change

	alignments = maxViterbiAlignment(corpus, t)

	p = average_sentence_score(baseline, alignments, precision)
	r = average_sentence_score(baseline, alignments, recall) 

	print "P:", p, "R:", r

	writeTranslationTableToFile(t)

	stop = time()
	print "Time spend:", int(stop - start + 0.5), "seconds"


