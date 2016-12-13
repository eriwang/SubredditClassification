from math import log

class Graph:
	def __init__(self, subreddit):
		print "Putting subreddit into graph form..."

		self.vertices = []
		self.verticesToVertexToEdgeWeight = {}

		self.maxNetUpvotes = subreddit.maxNetUpvotes
		self.minNetUpvotes = subreddit.minNetUpvotes

		# initialize vertices
		initScore = 1 / float(len(subreddit.idToItem))
		for id, item in subreddit.idToItem.iteritems():
			self.vertices.append(Vertex(id, initScore, self.getVertexWeight(item)))

		# calculate edge weights based on jaccard
		for i in range(len(self.vertices)):
			vertA = self.vertices[i]
			itemA = subreddit.idToItem[vertA.id]

			if i % 100 == 0:
				print "Calculating edge weights for vertex {} out of {}...".format(i, len(self.vertices))

			for j in range(i + 1, len(self.vertices)):
				vertB = self.vertices[j]
				itemB = subreddit.idToItem[vertB.id]
				sim = similarity(itemA.bodySet, itemB.bodySet)
				if sim > 0:
					self._addEdge(vertA, vertB, sim)

		print "Graph created!"

	def _addEdge(self, v1, v2, weight):
		if v1 not in self.verticesToVertexToEdgeWeight:
			self.verticesToVertexToEdgeWeight[v1] = {}
		if v2 not in self.verticesToVertexToEdgeWeight:
			self.verticesToVertexToEdgeWeight[v2] = {}

		self.verticesToVertexToEdgeWeight[v1][v2] = weight
		self.verticesToVertexToEdgeWeight[v2][v1] = weight

	def getVertexWeight(self, item):
		return float(item.netUpvotes - self.minNetUpvotes + 1) / float(self.maxNetUpvotes)

	def textRankIteration(self, d):
		i = 0
		for vertex, vertexToEdgeWeight in self.verticesToVertexToEdgeWeight.iteritems():
			if i % 100 == 0:
				print "Calculating TextRank for vertex {} out of {}...".format(i, len(self.vertices))

			sumIncomingTextRanks = 0
			for otherVertex, edgeWeight in vertexToEdgeWeight.iteritems():
				sumOutgoingWeights = sum(self.verticesToVertexToEdgeWeight[otherVertex].values())
				sumIncomingTextRanks += edgeWeight * otherVertex.lastScore / sumOutgoingWeights
			vertex.score = sumIncomingTextRanks * log(vertex.vertexWeight)
			i += 1

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

def similarity(wordSet1, wordSet2):
	# This is to avoid a division by 0 error
	if len(wordSet1) <= 1 or len(wordSet2) <= 1:
		return 0

	numSameWords = len(wordSet1.intersection(wordSet2))

	if numSameWords <= 0.05 * max(len(wordSet1), len(wordSet2)):
		return 0

	return float(numSameWords) / (log(len(wordSet1)) + log(len(wordSet2)))