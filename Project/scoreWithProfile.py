from readers import *
from plotter import *
import shelve

def score(sentence, differences):
	score = 0
	differencesKeys = differences.keys()
	for word, tag in sentence:
		if tag in differencesKeys:
			counting = differences[tag]
			if word in counting:
				score+=counting[word]

	score = score / float(len(sentence))

	return score

def scoreSentences(sentences, differencesEN, differencesES):
	results = []
	difen = dict()
	difes = dict()
	for key in differencesEN:
		difen[key] = differencesEN[key]
	for key in differencesES:
		difes[key] = differencesES[key]

	for i, sentencePair in enumerate(sentences):
		bool = sentencePair[0]
		en = sentencePair[1][0]
		es = sentencePair[1][1]
		
		scoreEN = score(en, difen)
		scoreES = score(es, difes)

		finalScore = (scoreEN + scoreES) / float(2)
		results.append((bool, finalScore))
	resultsSorted = sorted(results, key = lambda x: x[1], reverse=True)
	return resultsSorted

if __name__ == "__main__":	
	
	print "Reading difference files"
	differencesSoftwareEN = shelve.open("profiles/software_difference_profile.en")
	differencesLegalEN = shelve.open("profiles/legal_difference_profile.en")
	differencesSoftwareES = shelve.open("profiles/software_difference_profile.es")
	differencesLegalES = shelve.open("profiles/legal_difference_profile.es")
	
	# check if the required files were created properly
	if len(differencesSoftwareEN.keys()) == 0 or len(differencesLegalEN.keys()) == 0 or len(differencesSoftwareES.keys()) == 0 or len(differencesLegalES.keys()) == 0 :
		print "The required files were not yet created."
	
	else:
		print "Reading corpus files"	
		((mixedLegal, legal_mixed), (mixedSoftware, software_mixed)) = read_datasets(descriminative=True, tagTuples=True)
		legal_mixed = 0
		software_mixed = 0

		print "Computing results for legal"
		resLegal = scoreSentences(mixedLegal, differencesSoftwareEN, differencesSoftwareES)
		for i in range(2500):
			print resLegal[i]
			
		plot_retreival([x[0] for x in resLegal])

		print "Computing results for software"
		resSoftware = scoreSentences(mixedSoftware, differencesLegalEN, differencesLegalES)
		plot_retreival([x[0] for x in resSoftware])
		print "Done!"

	