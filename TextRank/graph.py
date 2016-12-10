class Graph:
	def __init__(self, subreddit):
		print "Putting subreddit into graph form..."

		self.vertices = []
		self.verticesToVertexToEdgeWeight = {}

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

	def _addEdge(self, v1, v2, weight):
		if v1 not in self.verticesToVertexToEdgeWeight:
			self.verticesToVertexToEdgeWeight[v1] = {}
		if v2 not in self.verticesToVertexToEdgeWeight:
			self.verticesToVertexToEdgeWeight[v2] = {}

		self.verticesToVertexToEdgeWeight[v1][v2] = weight
		self.verticesToVertexToEdgeWeight[v2][v1] = weight

	def textRankIteration(self, d):
		for vertex, vertexToEdgeWeight in self.verticesToVertexToEdgeWeight.iteritems():
			sumIncomingTextRanks = 0
			for otherVertex, edgeWeight in vertexToEdgeWeight.iteritems():
				sumOutgoingWeights = sum(self.verticesToVertexToEdgeWeight[otherVertex].values())
				sumIncomingTextRanks += edgeWeight * otherVertex.lastScore / sumOutgoingWeights
			vertex.score = sumIncomingTextRanks

		self._updateVertexScores()

	def _updateVertexScores(self):
		for vertex in self.vertices:
			vertex.lastScore = vertex.score

	def getTopNVertices(self, n):
		self.vertices.sort(key = lambda vertex: vertex.score)
		return self.vertices[0:n]


class Vertex:
	def __init__(self, id, score, vertexWeight):
		self.id = id
		self.lastScore = score
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