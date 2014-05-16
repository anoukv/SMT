from math import sqrt


def normalize_vector(vec):
	total = sqrt( sum([v**2 for v in vec.values()]) )
	for key in vec.keys():
		vec[key] = vec[key] / total
	return vec

def vector_similarity(vec1, vec2):
	intersection = set(vec1.keys()).intersection(set(vec2.keys()))
	return sum([ vec1[elem] * vec2[elem] for elem in intersection ])

def vector_distance(vec1, vec2):
	return 1 - vector_similarity(vec1, vec2)