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
def coverage(phraseTable1, phraseTable2, n=3):

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
		index = 0

		if queue == test:
			return True, index

		index = len(test)
		while index < len(allowed):
			del queue[0]
			index += 1
			queue.append(allowed[index])
			index += 1
			if queue == test:
				return True, index
		return False, index

	def findStart(start, dict):
		returnList = []
		for tup in dict:
			if tup[0] == start:
				returnList.append(tup)
		return returnList

	coverage = 0
	
	# for every phrase in phraseTable2	
	for phrasePair2 in prhaseTable2:
		
		p21 = phrasePair2[0]
		p22 = phrasePair2[1]
		
		considerable = set()
		found = False
		
		spanDict = defaultdict(set)
		# go over all phrasePairs in phraseTable1
		for phrasePair1 in prhaseTable1:
			
			# if it is in there, that's good, it's covered
			if phrasePair1 in phraseTable1:
				coverage += 1
				found = True
				break
			
			# else we are going to build a set of phrase pairs that are considerable
			else:
				p11 = phrasePair[0]
				p12 = phrasePair[1]
				
				# a phrase pair is considerable if it only contains elements that are 
				# in the phrase pair that we are looking for and the phrase pairs are a 
				# sequence (what I call a proper subset) of phrase pairs 2
				if containsOnly(p11, p21) and containsOnly(p12, p22):
					(status1, index1) = properSubset(p11, p21)
					(status2, index2) = properSubset(p12, p22)
 					if status1 and status2:
 						end1 = index1 + len(p11) - 1
 						end2 = index2 + len(p12) - 1
						considerable.add((phrasePair1, index1, end1, index2, end2))
						spanDict[(index1, end1)].add((index2, end2))		
		
		# if it was not found right away, we will try to rebuild it using the spanDict
		if not found:

			# the set of expandable things, i.e. initially starting points
			expandable = set(findStart(0, spanDict))
			
			# will keep track of the expansion choices for backtracking
			choices = defaultdict(set)
			
			# keeps track of the things that were expanded
			expanded = set()
			
			# keeps track of where the successes came from
			succes = defaultdict(set)

			# as long as there are still things to be expanded
			while len(expandable) > 0:
				# create new expandable set
				newExpandable = set()
				# for every starting point
				for startingPoint in expandable:
					# remember that it has been expanded
					expanded.add(startingPoint)
					
					# find blocks that continue using this starting point
					new = findStart(startingPoint[1]+1, spanDict)
					
					# for every found next block
					for item in new:

						# if this reaches the end of the sequence, it's a succes
						# and we need to keep track of it
						if item[1] == (len(p21) -1):
							succes[item].add(startingPoint)

						# register choosing this block at this point
						choices[startingPoint].add(item)
						# if the item has not been expanded, add it to the new expandables
						
						if item not in expanded:
							newExpandable.add(item)
				# put newExpandable in expandable
				expandable = newExpandable

	return coverage

	