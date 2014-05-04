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

a = [1, 2, 3]
b = [1, 5, 1, 2, 3]

print properSubset(a, b)