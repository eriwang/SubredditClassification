import nltk

from graph import Graph
from subreddit import Subreddit

def main():
	subreddit = Subreddit("Data/test_small.xml")
	graph = Graph(subreddit)
	print graph.verticesToEdgeWeight
	print len(graph.verticesToEdgeWeight)

if __name__ == "__main__":
	main()
