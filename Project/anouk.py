from readers import *
from sklearn import svm

def shortestLongsetWord(sentence):
	lengths = sorted(map(lambda x: len(x), sentence))
	shortest = lengths[0]
	longest = lengths[-1]
	return shortest, longest

def averageWordLenght(sentence):
	return reduce(lambda x, y: x + len(y), sentence, 0) / float(len(sentence))

def constructBasicFeatures(sentences, label):
	featureRepresentation = []
	labels = []
	for sentence in sentences:
		
		features = []
		
		# lenght of the sentence
		features.append(len(sentence))
		
		#average word lenght
		features.append(averageWordLenght(sentence))
		
		# lenght of shortest and longest word
		shortest, longest = shortestLongsetWord(sentence)
		features.append(shortest)
		features.append(longest)
		
		# append feature list
		featureRepresentation.append(features)
		
		#append label
		labels.append(label)
	
	return featureRepresentation, labels

def getUniqueEnglishWords(pairs):
	englishWords = set()
	for tup in pairs:
		for word in tup[0]:
			englishWords.add(word)
	return englishWords

if __name__ == "__main__":
	pairsSoftware = read_sentences('software', False)
	pairsLegal = read_sentences('legal', False)
	software = [x[0] for x in pairsSoftware]
	legal = [x[0] for x in pairsLegal]
	featuresSoftware, labelsSoftware = constructBasicFeatures(software, 1)
	featuresLegal, labelsLegal = constructBasicFeatures(legal, -1)
	trainingFeatures = featuresSoftware + featuresLegal
	trainingLabels = labelsSoftware + labelsLegal
	classifier = svm.SVC()
	classifier.fit(trainingFeatures, trainingLabels)

	print "Done!"

	

