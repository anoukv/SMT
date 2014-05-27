from readers import read_datasets
from feature_extraction import sentence_vector
from utils import vector_distance


from random import choice, sample
from collections import defaultdict
from math import sqrt
from multiprocessing import Pool
from time import time

class cluster:
	def __init__(self, center = dict() ):
		self.center = center
		self.elements_set = set(center.keys())
		self.assigned_datapoints = []
		self.class_count = (0,0)

	def add_datapoint(self, datapoint):
		self.assigned_datapoints.append(datapoint)

	def distance(self, data_point):
		return vector_distance(self.center, data_point)

	def cluster_distance(self, other_cluster):
		return self.distance(other_cluster.get_representation())

	def get_representation(self):
		if len(self.assigned_datapoints) > 0:
			self.set_new_cluster_center()
		return self.center

	def get_class_count(self):
		return self.class_count

	def set_new_cluster_center(self):
		def normalize_coc(coc):
			total = sqrt( sum([v**2 for v in coc.values()]) )
			new_coc = dict()
			for key in coc.keys():
				new_coc[key] = coc[key] / total
			return new_coc

		assert len(self.assigned_datapoints) > 0, "No data_points were assigned to this cluster..."
		new_center = defaultdict(float)
		class_count = [0,0]
		for data_point in self.assigned_datapoints:
			for element in data_point[1].keys():
				new_center[element] += data_point[1][element]
			if data_point[0]:
				class_count[0] += 1
			else:
				class_count[1] += 1
		new_center = normalize_coc(new_center)
		diff = vector_distance(new_center, self.center)
		self.center = new_center 
		self.assigned_datapoints = []
		self.class_count = tuple(class_count)
		self.elements_set = set(self.center.keys())
		return diff

def kmeans_process(data, k=100, min_dist_change=0.01, max_iter=8):
	def kmeans(data, k, min_dist_change=10, max_iter=8):
		clusters = dict()

		# init empty clusters
		for i in xrange(k):
			clusters[i] = cluster()

		# Fill clusters
		for i in xrange(len(data)):
			clusters[choice(xrange(k))].add_datapoint(data[i])

		# Calculate centroids
		for i in xrange(k):
			clusters[i].set_new_cluster_center()

		for _ in xrange(max_iter):
			print "\t\tIteration:", _
			# Assign data to clusters
			for datapoint in data:
				smallestDistance = 2
				smallestClusterIndex = -1
				for i in xrange(k):
					distance = clusters[i].distance(datapoint[1])
					if distance < smallestDistance:
						smallestDistance = distance
						smallestClusterIndex = i
				assert not smallestClusterIndex == -1, "Didn't find appropriate distance..."
				clusters[smallestClusterIndex].add_datapoint(datapoint)

			# re-estimate centers.
			diff = sum([ clusters[i].set_new_cluster_center() for i in xrange(k) ]) / float(k)
			print "\t\tDifference:", diff
			if min_dist_change > diff:
				print "\t\t\tBreaking after iteration", _
				break
		return clusters.values()

	# return kmeans(data, 1, 1, 1)
	return kmeans(data, k, min_dist_change, max_iter)
	
def NN(verbose=True):
	def score_sentences(mixed, clusters):
		def sentence_score((b, vec), clusters):
			results = [ (x.distance(vec), x.get_class_count()) for x in clusters ]
			(dist, best_batch) = (99, None)
			for (d,bb) in results:
				if d < dist:
					dist = d
					best_batch = bb
			return (b, best_batch[0] / float(sum(best_batch)) )
		results = [ sentence_score(s, clusters) for s in mixed ] 
		return [ x[0] for x in sorted(results, key = lambda x : x[1], reverse=True) ]

	start = time()
	print "Loading data..."
	data = read_datasets(descriminative=True, development=True, flat=True)
	normal_data = []
	for i in xrange(len(data)):
		for j in xrange(len(data[i])):
			normal_data.append(map(lambda x : (x[0], sentence_vector(x[1])), data[i][j]))
	data = ((normal_data[0], normal_data[1]),(normal_data[2], normal_data[3]))

	r = []
	for (mixed, train) in data:
		if verbose:
			print "\tTraining..."
		train = sample(train, len(train)/50)
		if verbose:
			print "\t\tTraining set size:", len(train)
		clusters = kmeans_process(train, 32)
		if verbose:
			print "\tScoring..."
		results = score_sentences(mixed, clusters)
		r.append(results)
		if verbose:
			print "\tIn:", len(filter(lambda x:x, results[:50000]))
			print "\tOut:", len(filter(lambda x:x, results[50000:]))
			print
	stop = time()
	print "Spend", int(stop-start+0.5), "seconds."
	return tuple(r)

if __name__ == '__main__':
	results = NN()

