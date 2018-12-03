import nltk
stop = nltk.corpus.stopwords.words("english")
def readFile(filename):
	ret = []
	file = open(filename, encoding="utf8", errors='ignore')
	lines = [line.rstrip('\n') for line in file]
	for line in lines:
		words = line.split()
		if len(words) > 1:
			append = words[1]
			if append not in stop and not words[0].startswith("@"):
				ret.append(append)
	return " ".join(ret)
print(readFile("./news_1985_671550.txt"))
print(readFile("./fic_2006_51066.txt"))