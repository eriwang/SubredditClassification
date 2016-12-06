import xml.etree.ElementTree as ET
import nltk

class Subreddit:
	def __init__(self, xmlFilename):
		tree = ET.parse(xmlFilename)
		subredditRoot = tree.getroot()

		self.displayName = subredditRoot.get("display_name")
		self.title = subredditRoot.get("title")
		self.submissions = []

		for submission in subredditRoot:
			self.submissions.append(Submission(submission))

class Submission:
	def __init__(self, submissionElement):
		self.body = submissionElement.get("self_body")
		self.netUpvotes = int(submissionElement.get("upvotes")) - int(submissionElement.get("downvotes"))
		self.replies = []

		for reply in submissionElement:
			print len(self.replies)
			self.replies.append(Reply(reply))

class Reply:
	def __init__(self, replyElement):
		self.body = replyElement.get("body")
		self.netUpvotes = replyElement.get("upvotes")
		self.replies = []

		for reply in replyElement:
			print "\treply to reply appended"
			self.replies.append(Reply(reply))

subreddit = Subreddit("Data/test_small.xml")
