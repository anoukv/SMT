from collections import defaultdict


def read_sentences_from_file(filename):
	"""
		Reads sentences from file.
	"""
	f = open(filename, 'r')
	content = f.readlines()
	f.close()
	content = [ c.replace("\n","").split(" ") for c in content ]
	content = [ [ y for y in x if y not in ["", " "] ] for x in content ]
	return filter(lambda x : not len(x) == 0, content)

def read_word_allignment_dicts(filename="training/p2_training_symal.nlen"):
	"""
		Reads word allignments from file.
	"""
	f = open(filename, 'r')
	content = f.readlines()
	f.close()
	content = [ c.replace("\n","").split(" ") for c in content ]
	content = [ [ tuple(map(int,y.split("-"))) for y in x if y not in ["", " "] ] for x in content ]
	dict_content = []
	for line in content:
		d = defaultdict(set)
		for (x, y) in line:
			d[x].add(y)
		dict_content.append(dict(d))
	return dict_content

def invert_allignment(allignment):
	inv_allignment = defaultdict(set)
	for key, values in allignment.items():
		for value in values:
			inv_allignment[value].add(key)
	return dict(inv_allignment)