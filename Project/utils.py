from math import sqrt


def normalize_vector(vec):
	total = sqrt( sum([v**2 for v in vec.values()]) )
	for key in vec.keys():
		vec[key] = vec[key] / total
	return vec