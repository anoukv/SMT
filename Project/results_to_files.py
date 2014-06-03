from readers import read_datasets

def save_file(lines, name):
	f = open(name, 'w')
	for line in lines:
	    f.write("".join([ x + " " for x in line]) + "\n")
	f.close()

def save_results(results, filename="selected_sentences", data=None):
	print "Saving results.."
	if data==None:
		data = read_datasets(descriminative=True, development=True, flat=False)

	filename = "../../project3_data/results/" + filename
	data = (data[0][0], data[1][0])
	data = ([ x[1] for x in data[0]], [ x[1] for x in data[1]])
	results = ([ x[1] for x in results[0]], [x[1] for x in results[1]])
	
	legal = sorted(zip(results[0], data[0]), key = lambda x : x[0], reverse=True)[:50000]
	software = sorted(zip(results[1], data[1]), key = lambda x : x[0], reverse=True)[:50000]

	(legal_e, legal_s) = zip(*[ x[1] for x in legal ])
	(software_e, software_s) = zip(*[ x[1] for x in software ])

	save_file(legal_e, filename+".legal.en")
	save_file(legal_s, filename+".legal.es")
	save_file(software_e, filename+".software.en")
	save_file(software_s, filename+".software.es")


