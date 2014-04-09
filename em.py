


def loadData(f = "corpus.nl", e = "corpus.en"):
	fileo = open(f,'r')
	f = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	fileo = open(e,'r')
	e = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	return zip(f, e)

if __name__ == "__main__":
	print loadData()[0]
