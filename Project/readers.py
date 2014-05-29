from time import time
from utils import hypernize_sentence

def read_sentences(filename="legal", flat=False, meta_f=(tuple, tuple), ext=""):
	"""
		Reads sentence pairs a a given domain
		Returns a list of sentence tuples
	"""		
	filename = "../../project3_data/" + filename
	contents = []

	for (op, filename_) in zip(meta_f, (filename+".en"+ext, filename+".es"+ext)):
		f = open(filename_, 'r')
	 	content = map(lambda y : op(y.replace("\n","").split(" ")), filter(lambda x : len(x) > 1, f.readlines()))
	 	f.close()
	 	contents.append(content)

	content = zip(contents[0], contents[1])
	if flat:
		return map(lambda x : x[0] + x[1], content)
	else:
		return content

def read_datasets(descriminative=False, development=True, flat=False, meta_f=(tuple, tuple), ext=""):
	"""
		Reads development or test set, for normal or descriminative analises
		Returns:
			Tuple of two datasets, development or test
			Each of which is a tuple of (mixed, other)
				if descriminative:
					len(mixed) == 450.000
					other = 100.000 tuples of (Bool, sentence)
					where bool indicates pos, neg example
				else:
					len(mixed) == 500.000
					other = 50.000 positive sentences
				if flat:
					sentences = a tuple of all words in both languages
				else:
					sentences = (english, spanish)
				if hype:
					applies hypernize_sentence to english sentences
	"""

	if development:
		domains = ["legal", "software"]
	else:
		domains = ["legal.test", "software.test"]

	print "  Reading main.."
	out = read_sentences("out", flat, meta_f, ext)
	print "  Reading rest.."
	in1 = read_sentences(domains[0], flat, meta_f, ext)
	in2 = read_sentences(domains[1], flat, meta_f, ext)
	
	mark_false = lambda x : (False, x)
	mark_true = lambda x : (True, x)
	out = map(mark_false, out)
	in1 = map(mark_true, in1)
	in2 = map(mark_true, in2)

	if descriminative:
		pos1 = in1[:50000]
		pos2 = in2[:50000]
		neg1 = out[:50000]
		neg2 = out[:50000]
		mixed1 = out[50000:] + in1[50000:]
		mixed2 = out[50000:] + in2[50000:]
		return ((mixed1, pos1+neg1), (mixed2, pos2+neg2))
	else:
		mixed1 = out + in1[:50000]
		mixed2 = out + in2[:50000]
		return ((mixed1, in1[50000:]), (mixed2, in2[50000:]))

if __name__ == '__main__':
	start = time()
	read_datasets()
	stop = time()
	print stop - start




