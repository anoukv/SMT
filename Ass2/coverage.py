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

		if queue == test:
			return True

		index = len(test)
		while index < len(allowed):
			del queue[0]
			queue.append(allowed[index])
			index += 1
			if queue == test:
				return True
		return False

	coverage = 0
	
	# for every phrase in phraseTable2	
	for phrasePair2 in prhaseTable2:
		
		p21 = phrasePair2[0]
		p22 = phrasePair2[1]
		
		considerable = set()
		found = False
		
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
					if properSubset(p11, p21) and properSubset(p12, p22):
						considerable.add(phrasePair1)
		
		# if it was not found right away, we will try to rebuild it using considerable
		# start at the beginning and build it up.
		# early stopping for lenght constraints? 
		# isThisOk will check whether this is a valid next building block. 
		# don't know yet how to do this correctly and efficiently 
		if not found:
			# try to build it
			firsts = set()
			for potentialFirst in considerable:
				if isThisOk(phrasePair2, potentialFirst):
					firsts.add(potentialFirst)

	return coverage

	def isThisOk(whatWeNeed, whatWeGet):
		return whatWeNeed[0][:len(whatWeGet[0])] == whatWeGet[0] and whatWeNeed[1][:len(whatWeGet[1])] == whatWeGet[1]
