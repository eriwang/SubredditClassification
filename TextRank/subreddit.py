from nltk.tokenize import word_tokenize

import xml.etree.ElementTree as ET

class Subreddit:
	def __init__(self, xmlFilename):
		print "Beginning to parse {}...".format(xmlFilename)
		tree = ET.parse(xmlFilename)
		subredditRoot = tree.getroot()

		self.displayName = subredditRoot.get("display_name")
		self.title = subredditRoot.get("title")
		self.submissions = []

		for submission in subredditRoot:
			self.submissions.append(Submission(submission))

		print "Parsing complete!"

class Submission:
	def __init__(self, submissionElement):
		self.body = submissionElement.get("self_body")
		self.bodySet = bodyToTokens(self.body)
		self.netUpvotes = int(submissionElement.get("upvotes")) - int(submissionElement.get("downvotes"))
		self.replies = []
		self.id = submissionElement.get("id")

		for reply in submissionElement:
			self.replies.append(Reply(reply))

class Reply:
	def __init__(self, replyElement):
		self.body = replyElement.get("body")
		self.bodySet = bodyToTokens(self.body)
		self.netUpvotes = replyElement.get("upvotes")
		self.replies = []
		self.id = replyElement.get("id")

		for reply in replyElement:
			self.replies.append(Reply(reply))

def bodyToTokens(body):
	tokens = word_tokenize(body)
	return set([t.lower() for t in tokens])