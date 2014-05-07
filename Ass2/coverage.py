# Computing the coverage
# assumes that ([1, 2, 3], [3, 4, 5])
# not sure if this will be like this

# returns percentage of phrases in phraseTable2 that are in phraseTable1	
def coverageSimple(phraseTable1, phraseTable2):
	phrases1 = set(phraseTable1.keys())
	phrases2 = set(phraseTable2.keys())
	numberOfPhrasesInCommon = len(phrases1.intersection(phrases2))
	return numberOfPhrasesInCommon * 100 / float(len(phrases2))

# returns percentage of phrases in phraseTable2 that can be built from phrases in 1
def coverage(phraseTable1, phraseTable2, configuration_size=3):

	# returns True if test only contains elements from allowed, false otherwise
	def containsOnly(test, allowed):
		for elem in test:
			if elem not in allowed:
				return False
		return True

	# returns true if test is a subsequence of allowed, false otherwise
	def properSubset(test, allowed):
		# for debugging later
		if len(allowed) <= len(test):
			print "problem 1"
		
		queue = allowed[:len(test)]

		if queue == test:
			return True, 0

		i = len(test)
		while i < len(allowed):
			del queue[0]
			i += 1
			queue.append(allowed[i])
			if queue == test:
				return True, i - len(test)
		return False, -1

	def findStart(start, dict):
		# return [ tup for tup in dict if tup[0] == start ]
		returnList = []
		for tup in dict:
			if tup[0] == start:
				returnList.append(tup)
		return returnList

	coverage = 0
	
	# for every phrase in phraseTable2	
	for phrasePair2 in phraseTable2:
		# if it is in there, that's good, it's covered
		if phrasePair2 in phraseTable1:
			coverage += 1

		else:
			# if it was not found right away, we will try to rebuild it using the spanDict
			spanDict = defaultdict(set)
			# go over all phrasePairs in phraseTable1
			p21 = phrasePair2[0]
			p22 = phrasePair2[1]

			for phrasePair1 in phraseTable1:
				p11 = phrasePair1[0]
				p12 = phrasePair1[1]
				
				# a phrase pair is considerable if it only contains elements that are 
				# in the phrase pair that we are looking for and the phrase pairs are a 
				# sequence (what I call a proper subset) of phrase pairs 2
				if containsOnly(p11, p21) and containsOnly(p12, p22):
					(status1, index1) = properSubset(p11, p21)
					(status2, index2) = properSubset(p12, p22) # This can be optimized
					# let's not care about the end point for now...
 					if status1 and status2 and index1 == index2:
 						end1 = index1 + len(p11) - 1
 						end2 = index2 + len(p12) - 1
						spanDict[(index1, end1)].add((index2, end2))		
			

			# the set of expandable things, i.e. initially starting points
			expandable = set(findStart(0, spanDict))
			
			# keeps track of the things that were expanded
			expanded = set()
			
			# define the goal
			goal = len(p21) - 1
			
			breakAllLoops = False
			# as long as there are still things to be expanded
			for _ in xrange(configuration_size):

				if breakAllLoops:
					break

				# create new expandable set
				newExpandable = set()
				
				# for every starting point
				for startingPoint in expandable:

					if breakAllLoops:
						break
					
					# remember that it has been expanded
					expanded.add(startingPoint)
					
					# find blocks that continue using this starting point
					new = findStart(startingPoint[1]+1, spanDict)
					
					# for every found next block
					for item in new:
						if item[1] == goal:
							breakAllLoops = True
							coverage += 1
							break
						# if the item has not been expanded, add it to the new expandables
						if item not in expanded:
							newExpandable.add(item)

				# put newExpandable in expandable
				expandable = newExpandable

	return coverage * 100 / float(len(phraseTable2))

	