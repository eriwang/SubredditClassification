def jaccardSimilarity(wordSet1, wordSet2):
	numSameWords = len(wordSet1.intersection(wordSet2))
	numWordsTotal = len(wordSet1.union(wordSet2))
	return float(numSameWords) / float(numWordsTotal)