# coverage_bf tries a brute force method to find allignments.

from collections import defaultdict
from copy import copy

def starts_are_same(seq1, seq2):
	length = min(len(seq1), len(seq2))
	return tuple(seq1[:length]) == tuple(seq2[:length])

def generator((phrase_left, phrase_right), (build_left, build_right), choices):
	if tuple(build_left) == phrase_left and tuple(build_right) == phrase_right:
		return True
	if len(build_left) >= len(phrase_left) or len(build_right) >= len(phrase_right):
		return False
	for choice in choices:
		new_left, new_right = copy(build_left), copy(build_right)
		for elem in choice[0]:
			new_left.append(elem)
		for elem in choice[1]:
			new_right.append(elem)

		if starts_are_same(phrase_left, new_left) and starts_are_same(phrase_right, new_right):
			if generator((phrase_left, phrase_right), (new_left, new_right), choices):
				return True
	return False

def coverage_bf(phraseTable1, phraseTable2, configuration_size=4):
	covered = 0
	left = set(phraseTable1.keys())
	right = set(phraseTable2.keys())
	for phrase in right:
		if phrase in left or generator(phrase, ([],[]), right):
			covered += 1

	return covered * 100 / float(len(right))
