from nltk.corpus import stopwords as stopwords
from nltk.tokenize import word_tokenize

import string
import sys
import xml.etree.ElementTree as ET

stopwordSet = set(stopwords.words("english"))
punctuationSet = set(list(string.punctuation))

class Subreddit:
	def __init__(self, xmlFilename):
		print "Beginning to parse {}...".format(xmlFilename)
		tree = ET.parse(xmlFilename)
		subredditRoot = tree.getroot()

		self.maxNetUpvotes = 1
		self.minNetUpvotes = 1

		self.displayName = subredditRoot.get("display_name")
		self.title = subredditRoot.get("title")
		self.submissions = []

		self.idToItem = {}

		for submission in subredditRoot:
			self.submissions.append(Submission(submission, self))

		print "Parsing complete!"

	def addItem(self, id, item):
		if id in self.idToItem:
			sys.stderr.write("Duplicate id {}".format(id))
			sys.exit(1)

		self.idToItem[id] = item
		if item.netUpvotes > self.maxNetUpvotes:
			self.maxNetUpvotes = item.netUpvotes
		elif item.netUpvotes < self.minNetUpvotes:
			self.minNetUpvotes = item.netUpvotes

class Submission:
	def __init__(self, submissionElement, subreddit):
		self.body = submissionElement.get("title") + "\n" + submissionElement.get("self_body")
		self.bodySet = bodyToTokens(self.body)
		self.netUpvotes = int(submissionElement.get("upvotes")) - int(submissionElement.get("downvotes"))
		self.replies = []
		self.id = submissionElement.get("id")

		subreddit.addItem(self.id, self)

		for reply in submissionElement:
			self.replies.append(Reply(reply, subreddit))

class Reply:
	def __init__(self, replyElement, subreddit):
		self.body = replyElement.get("body")
		self.bodySet = bodyToTokens(self.body)
		self.netUpvotes = int(replyElement.get("upvotes"))
		self.replies = []
		self.id = replyElement.get("id")

		subreddit.addItem(self.id, self)

		for reply in replyElement:
			self.replies.append(Reply(reply, subreddit))

def bodyToTokens(body):
	tokens = word_tokenize(body)
	return set([t.lower() for t in tokens if t.lower() not in stopwordSet and t not in punctuationSet])