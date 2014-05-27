from readers import *
from profileUtils import *
from plotter import *
import shelve

def getResults(mixedTaggedCorpus, differences):
	scoredSentences = scoreSentences(mixedSoftwareTagged, differencesSoftware)
	res = [(scoredSentences[i][0], mixedSoftware[i][0]) for i in xrange(len(scoredSentences))]
	sortedRes = sorted(res, key = lambda x: x[0], reverse=True)
	bools = [res[1] for res in sortedRes]
	return bools	

def scoreSentences(sentences, differences):
	scoredSentences = []
	for sen in sentences:	
		score = 0
		for word, tag in sen:
			if tag in differences:
				counting = differences[tag]
				if word in counting:
					score += counting[word]

		# if the score is smaller than 0, readjust to zero
		if score <= 0:
			score = 0
		
		# otherwise, normalize
		else:
			score = score / float(len(sen))

		# add tuple score, taggedSentence to scoredSentences
		scoredSentences.append((score, sen))
	return scoredSentences

if __name__ == "__main__":
	domain = "software"
	
	differencesSoftware = shelve.open("profiles/software_difference_profile")
	differencesLegal = shelve.open("profiles/legal_difference_profile")

	# check if the required files were created properly
	if len(differencesSoftware.keys()) == 0 or len(differencesLegal.keys()) == 0:
		print "The required files were not yet created."
	
	else:	
		((mixedLegal, legal_mixed), (mixedSoftware, software_mixed)) = read_datasets(descriminative=True)
		
		mixedLegalTagged = getTaggedEnglishCorpus(mixedLegal)
		mixedSoftwareTagged = getTaggedEnglishCorpus(mixedSoftware)
		resSoftware = getResults(mixedSoftwareTagged, differencesSoftware)
		resLegal = getResults(mixedLegalTagged, differencesLegal)
		plot_retreival(resSoftware)

	