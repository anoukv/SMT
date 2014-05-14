
# Anouk? Even overleggen
def precision_recall_calculator(results):
	precisions = []
	recalls = []

	good = 0
	for i in xrange(50000):
		if results[i]:
			good += 1
		precisions.append( good / float(i) )
		recalls.append( good / float(i) )
	for i in xrange(50000, len(results)):
		if results[i]:
			good += 1
		recalls.append( good / 50000 )
