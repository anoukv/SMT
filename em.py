


def loadData(f = "corpus.nl", e = "corpus.en"):
	fileo = open(f,'r')
	f = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	fileo = open(e,'r')
	e = map(lambda x : x.replace("\n","").split(" "), fileo.readlines())
	fileo.close()

	return (f, e)

def initializeT(coprus):
	translationProbs = dict()
	
	for sentencePair in coprus:
		for f in sentencePair[0]:
			for e in sentencePair[1]:
				translationProbs[(f, e)] = 1
	return translationProbs

if __name__ == "__main__":
	print loadData()[0][:5]
