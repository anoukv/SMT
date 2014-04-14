

def read_vit(filename="viterbi.small"):
	f = open(filename,'r')
	lines = f.readlines()
	f.close()

	sentence_count = len(lines) / 3
	sentences = []
	for _ in xrange(sentence_count):
		# This line is bs
		lines.pop(0)

		# For first line, create a map of 'index' => word
		firstline = filter(lambda x : not x == "", lines.pop(0).replace("\n","").split(" "))
		firstline = dict(zip(xrange(1,len(firstline)+1), firstline))

		# For second line, 
		secondline = map(lambda x : (x[0].replace(" ",""), map(int, filter(lambda x : not x == "", x[1].split(" ")))), filter(lambda x : len(x) == 2, map(lambda x : x.split("({"), lines.pop(0).replace("\n","").split("})"))))

		# print firstline
		# print secondline
		
		pairs = []
		for (word, froms) in secondline:
			for index in froms:
				pairs.append((firstline[index], word))

		sentences.append(pairs)
	
	return sentences
		






if __name__ == "__main__":
	read_vit()


