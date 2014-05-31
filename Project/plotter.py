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

if __name__ == '__main__':
	print "Loading results.."
	from results_counting_scores_extended_5 import results
	print "Plotting.."
	plot_retreival(map(lambda x : x[0], results[0]))
	plot_retreival(map(lambda x : x[0], results[1]))