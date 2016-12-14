import sys

from graph import Graph
from subreddit import Subreddit

def runTextRankOnGraph(graph, iterations, d):
	for i in range(iterations):
		graph.textRankIteration(d)

def main():
	subreddit = Subreddit(sys.argv[1])
	graph = Graph(subreddit)
	runTextRankOnGraph(graph, 1, 0.85)

	top5Vertices = graph.getTopNVertices(5)

	print " ".join([subreddit.idToItem[v.id].body for v in top5Vertices])

if __name__ == "__main__":
	main()
