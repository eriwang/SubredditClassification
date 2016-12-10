import nltk

from graph import Graph
from subreddit import Subreddit

def runTextRankOnGraph(graph, iterations, d):
	for i in range(iterations):
		graph.textRankIteration(d)

def main():
	subreddit = Subreddit("Data/test_small.xml")
	graph = Graph(subreddit)
	runTextRankOnGraph(graph, 1, 0.85)

	top10Vertices = graph.getTopNVertices(10)

	print "\n".join([subreddit.idToItem[v.id].body for v in top10Vertices])

if __name__ == "__main__":
	main()
