class Vertex:
	def __init__(self):
		self.id = ""
		self.score = 0
		self.vertexWeight = 0
		self.vertexToEdgeWeight = {}

def jaccardSimilarity(wordSet1, wordSet2):
	numSameWords = len(wordSet1.intersection(wordSet2))
	numWordsTotal = len(wordSet1.union(wordSet2))
	return float(numSameWords) / float(numWordsTotal)

