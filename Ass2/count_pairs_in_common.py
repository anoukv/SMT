
def read_own_pairs(filename="../../cocs.our"):
	f = open(filename, 'r')
	all_pairs = set(map(lambda x : x.replace(" \n",""), filter(lambda x : len(x) > 3, f.readlines())))
	f.close()
	return all_pairs

def read_gold_pairs(filename="../../goldStandardPhraseTable"):
	all_pairs = set()
	f = open(filename, 'r')
	for line in f.readlines():
		if len(line) > 3:
			line = line.split(" ||| ")
			line = line[0] + " ||| " + line[1]
			all_pairs.add(line)
	f.close()
	return all_pairs

if __name__ == '__main__':
	print "Reading own pairs..."
	our = read_own_pairs()
	print "Reading gold pairs..."
	gold = read_gold_pairs()
	print "Results:"
	print "Recall:", len(our.intersection(gold)) / float(len(gold))
	print "Precision:", len(our.intersection(gold)) / float(len(our))
