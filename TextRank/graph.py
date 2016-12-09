class Graph:
	def __init__(self, subreddit):
		print "Putting subreddit into graph form..."

		self.vertices = []
		self.verticesToEdgeWeight = {}

		# initialize vertices
		initScore = 1 / float(len(subreddit.idToItem))
		for id, item in subreddit.idToItem.iteritems():
			self.vertices.append(Vertex(id, initScore, getVertexWeight(item)))

		# calculate edge weights based on jaccard
		for i in range(len(self.vertices)):
			vertA = self.vertices[i]
			itemA = subreddit.idToItem[vertA.id]

			if i % 100 == 0:
				print "Calculating edge weights for vertex {} out of {}...".format(i, len(self.vertices))

			for j in range(i + 1, len(self.vertices)):
				vertB = self.vertices[j]
				itemB = subreddit.idToItem[vertB.id]
				similarity = jaccardSimilarity(itemA.bodySet, itemB.bodySet)
				if similarity > 0:
					self._addEdge(vertA, vertB, similarity)

		print "Graph created!"

	def _getVertexKey(self, v1, v2):
		if v1.id < v2.id:
			return v1.id + v2.id
		else:
			return v2.id + v1.id

	def _addEdge(self, v1, v2, weight):
		self.verticesToEdgeWeight[self._getVertexKey(v1, v2)] = weight

	def _getEdge(self, v1, v2):
		key = self._getVertexKey(v1, v2)
		if key in self.verticesToEdgeWeight:
			return self.verticesToEdgeWeight[key]
		else:
			return 0

class Vertex:
	def __init__(self, id, score, vertexWeight):
		self.id = id
		self.score = score
		self.vertexWeight = vertexWeight

# TODO: use features to create a "weight" for the vertex
def getVertexWeight(item):
	return 0

def jaccardSimilarity(wordSet1, wordSet2):
	numSameWords = len(wordSet1.intersection(wordSet2))

	if numSameWords <= 0.05 * max(len(wordSet1), len(wordSet2)):
		return 0

	numWordsTotal = len(wordSet1.union(wordSet2))
	return float(numSameWords) / (float(numWordsTotal) if numWordsTotal > 0 else 1)