
# 
def precision_recall_calculator(results):
	precisions = []
	recalls = []

	maxx = 50000.0
	good = 0
	for i in xrange(maxx):
		if results[i]:
			good += 1
		precisions.append( good / float(i) )
		recalls.append( good / maxx )

	# for i in xrange(maxx, len(results)):
	# 	if results[i]:
	# 		good += 1
	# 	recalls.append( good / maxx )
	
