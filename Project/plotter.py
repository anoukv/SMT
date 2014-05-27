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