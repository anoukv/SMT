from readers import *
from plotter import *
import shelve

def score(sentence, differences):
	score = 0
	for word, tag in sentence:
		if tag in differences:
			counting = differences[tag]
			if word in counting:
				score+=counting[word]
	if score <= 0:
		score = 0
	else:
		score = score / float(sen(sentence))

	return score

def scoreSentences(sentences, differencesEN, differencesES):
	results = []
	for sentencePair in sentences:
		bool = sentencePair[0]
		en = sentencePair[1][0]
		es = sentencePair[1][1]
		
		scoreEN = score(en, differencesEN)
		scoreES = score(es, differencesES)

		score = (scoreEN + scoreES) / float(2)

		results.append((bool, score))
	resultsSorted = sorted(results, key = lambda x: x[1], reverse=True)
	return resultsSorted

if __name__ == "__main__":	
	
	differencesSoftwareEN = shelve.open("profiles/software_difference_profile.en")
	differencesLegalEN = shelve.open("profiles/legal_difference_profile.en")
	differencesSoftwareES = shelve.open("profiles/software_difference_profile.es")
	differencesLegalES = shelve.open("profiles/legal_difference_profile.es")
	
	# check if the required files were created properly
	if len(differencesSoftwareEN.keys()) == 0 or len(differencesLegalEN.keys()) == 0 or len(differencesSoftwareES.keys()) == 0 or len(differencesLegalES.keys()) == 0 :
		print "The required files were not yet created."
	
	else:	
		((mixedLegal, legal_mixed), (mixedSoftware, software_mixed)) = read_datasets(descriminative=True, tagTuples=True)

		resLegal = scoreSentences(mixedLegal, differencesSoftwareEN, differencesSoftwareES)
		resSoftware = scoreSentences(mixedSoftware, differencesLegalEN, differencesLegalES)

	