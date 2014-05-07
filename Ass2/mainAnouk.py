# Written by Anouk 
from utils import *

def doForSentencePair(sentence_e, sentence_f, alignmnent_f_e):
	
	for e_start in xrange(len(sentence_e)):
		for e_end in xrange(e_start, len(sentence_e)):
			print
			print "e_start, e_end", e_start, e_end

			f_start = len(sentence_f)
			f_end = 0
			print "Initial f_start, f_end", f_start, f_end
			
			for (e, f) in alignmnent_f_e:
				if e_start <= e and e <= e_end:
					#print "Alignment", (e, f)
					f_start = min(f, f_start)
					f_end = max(f, f_end)
					
					#print "New f_start, f_end", f_start, f_end
			#print "Final f_start, f_end", f_start, f_end, "for: e_start, e_end", e_start, e_end
			extract(f_start, f_end, e_start, e_end, alignmnent_f_e)
	return []

def extract(f_start, f_end, e_start, e_end, alignmnent_f_e):
	if f_end == 0:
		#print "Rejected"
		return []
	for (e, f) in alignmnent_f_e:
		if e < e_start or e > e_end:
			#print "Rejected"
			return []
	E = []
	f_s = f_start

	print "Not rejected!", f_start, f_end, e_start, e_end
	return []


if __name__ == "__main__":
	print "Reading data..."
	training = False
	heldout = False
	
	if training:
		allignment = read_word_allignment_dicts()
		s_f = read_sentences_from_file("training/p2_training.nl")
		s_e = read_sentences_from_file("training/p2_training.en")
	
	elif heldout:
		allignment = getAllignment("heldout/p2_heldout_symal.nlen")
		s_f = read_sentences_from_file("heldout/p2_heldout.nl")
		s_e = read_sentences_from_file("heldout/p2_heldout.en")
	
	#doForSentencePair(s_f[6], s_e[6], allignment[6])

	s_d = ["michael", "geht", "davon", "aus", ",", "dass", "er", "im", "haus", "bleibt"]
	s_e = ["michael", "assumes", "that", "he", "will", "stay", "in", "the", "house"]
	test = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 5), (3, 6), (4, 9), (5, 9), (6, 7), (7, 7), (8, 8)]

	doForSentencePair(s_e, s_d, test)

	# print allignment[6], s_f[6], s_e[6]


