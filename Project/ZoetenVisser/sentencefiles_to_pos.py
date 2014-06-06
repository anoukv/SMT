from pattern.en import tag as tagEN
from pattern.es import tag as tagES

def line_as_pos(line, tagger, app):
	try:
		return map(lambda x : x[1] + app, tagger(line))
	except:
		return [ str(len(sentence.split(" "))) + app ]

def transform_file(filename, tagger, app):
	infile = "../../project3_data/" + filename
	outfile = "../../project3_data/" + filename + ".pos"
	inf = open(infile, 'r')
	outf = open(outfile, 'w')
	for line in inf.readlines():
		line = "".join([ x + " " for x in line_as_pos(line, tagger, app) ]) + "\n"
		line = line.encode("utf8", 'ignore')
		outf.write(line)
	inf.close()
	outf.close()

def go():
	print "10 files to process..."
	i = 0
	for filename in ["legal.test", "software.test", "legal", "software", "out"]:
		i += 1
		print "File number:", i
		transform_file(filename + ".en", tagEN, "_en")
		i += 1
		print "File number:", i
		transform_file(filename + ".es", tagES, "_es")

if __name__ == '__main__':
	go()