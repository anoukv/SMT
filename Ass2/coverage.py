# Computing the coverage

# returns percentage of phrases in phraseTable2 that are in phraseTable1	
def coverageSimple(phraseTable1, phraseTable2):
	phrases1 = set(phraseTable1.keys())
	phrases2 = set(phraseTable2.keys())
	numberOfPhrasesInCommon = len(phrases1.intersection(phrases2))
	return numberOfPhrasesInCommon * 100 / float(len(phrases2))

def coverage(phraseTable1, phraseTable2, n=3):

	def extractAllWithTerms(phraseTable1, termsSource, termsTarget):
		result = set()
		for (source, target) in phraseTable1:
			if len(termsSource.intersection(set(source))) >  0 and len(termsTarget.intersection(set(target))) > 0:
				result.add((source, target))
		return result 

	coverage = 0
	for phrasePair in prhaseTable2:
		# check if it is already in there
		if phrasePair in phraseTable1:
			coverage += 1
		else:


		# check if we can build it


	return coverage
