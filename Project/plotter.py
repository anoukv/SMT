import matplotlib.pyplot as plt


def plot_retreival(bool_sequence, total=None):
	if total == None:
		total = len(filter(lambda x : x, bool_sequence))
	total = float(total)

	numbers = []
	goods = 0
	for b in bool_sequence:
		if b:
			goods += 1
		numbers.append(goods/total)

	plt.plot(numbers)
	plt.ylabel('Retreived')
	plt.xlabel('N - items returned')
	plt.show()

def plot_r(results):
	s1 = map(lambda x : x[0], results[0])
	s2 = map(lambda x : x[0], results[1])
	plot_results(s1, s2)

def plot_results(sequence1, sequence2, total=None):
	if total == None:
		total = len(filter(lambda x : x, sequence1))
	total = float(total)

	nums = []
	for sequence in (sequence1, sequence2):
		numbers = []
		goods = 0
		for b in sequence:
			if b:
				goods += 1
			numbers.append(goods/total)
		nums.append(numbers)

	numbers = []
	div = float(len(sequence1))
	for i in xrange(0, len(sequence1)):
		numbers.append(i/div)

	nums.append(numbers)

	fig, ax = plt.subplots()
	ax.plot(nums[0], label="Legal")
	ax.plot(nums[1], label="Software")
	ax.plot(nums[2], '--', label="Random")
	legend = ax.legend(loc="lower right", shadow=False)

	# p1 = plt.plot(nums[0], label="legal")
	# p2 = plt.plot(nums[1], label="software")
	# p3 = plt.plot(nums[2], '--', label="random")


	plt.ylabel('Retreived')
	plt.xlabel('N - items returned')
	plt.show()

if __name__ == '__main__':
	print "Loading.."
	from results_counting_scores_extended_3_200000 import results
	print "Plotting.."
	s1 = map(lambda x : x[0], results[0])
	s2 = map(lambda x : x[0], results[1])
	plot_results(s1, s2)



