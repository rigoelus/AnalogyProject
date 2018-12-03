
import nltk
stop = nltk.corpus.stopwords.words("english")
def readFile(filename):
	ret = []
	lines = [line.rstrip('\n') for line in open(filename)]
	for line in lines:
		words = line.split()
		if len(words) > 1:
			append = words[1]
			if append not in stop and not words[0].startswith("@"):
				ret.append(append)
	return " ".join(ret)
print(readFile("./wordLemPoS/news_1879_742950.txt"))
print(readFile("./wordLemPoS/news_1880_743450.txt"))

