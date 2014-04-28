# Computing the coverage

# returns percentage of phrases in phraseTable2 that are in phraseTable1	
def coverageSimple(phraseTable1, phraseTable2):
	phrases1 = set(phraseTable1.keys())
	phrases2 = set(phraseTable2.keys())
	numberOfPhrasesInCommon = len(phrases1.intersection(phrases2))
	return numberOfPhrasesInCommon * 100 / float(len(phrases2))

def coverage(phraseTable1, phraseTable1, n=3):
	coverage = 0
	return coverage
