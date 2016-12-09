# Brian Ma
# briandma

import sys
import operator
import math
import string
import re
import xml.etree.ElementTree as ET
from sklearn.tree import DecisionTreeClassifier
# from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
import sklearn
import datetime
from collections import Counter







# Open files
# fileList = open(sys.argv[1], "r").readlines()
# #test = open(sys.argv[2], "r")
# out = open(sys.argv[1] + ".out", "w")

# stopwordsFile = open("stopwords.txt", "r")
# stopwords = [line[:-1] for line in stopwordsFile]

# vocab = []
# titleVocab = []
# subredditVocab = []

### Overall features
# One hot encoding for words ( % of words that are that word)
# Frequency of question marks (% of tokens that are ?)
# Frequency of punctuation (% of tokens that are punct)
# Average length of word (?)
# Capitalized after . or ? (?)
# Number of sentences

### Post features
# Words in title
# Number of words in title [0]
# Length of title [1]
# Words in post 
# Number of words in post [2]
# Lenght of post [3]
# Number of new lines [4]
# Portion of words that are numbers [5]
# Link present, search for http or https or .com or www. [6]
# Portion of words in caps lock [7]

### If not predicting new post
# Upvotes
# Downvotes

### Comment related features
# Deepest reply [0]
# Number of comments
# Average number of words per comment / reply
# Portion of words that are numbers
# Number of words
# 

#Note: parse so that ....... is together which means .....? will also probalby be together
# Means instead of doing ==, gonna have to do find/in

# Depth 0 is the submission, 1 is first level comment
# def generateFeatures(post, featureVector, titleList, wordList, srVocab, totalNumbers=0, capsLock=0, totalWords=0):
# 	# bodyList = body.split() # TODO make this regex from p4
# 	if post.tag == "Submission":
# 		body = post.attrib["self_body"]
# 		bodyList =  re.findall(r"[0-9]+[.][0-9]+|[0-9,]+[.][0-9]+|[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+", body)
		
# 		title = post.attrib["title"]
# 		titleSplit =  re.findall(r"[0-9]+[.][0-9]+|[0-9,]+[.][0-9]+|[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+", title)
# 		# titleSplit = title.split() # TODO: regex?
# 		featureVector[0] = len(titleSplit)
# 		featureVector[1] = len(title)
# 		featureVector[2] = len(bodyList)
# 		featureVector[3] = len(body)

# 		for word in titleSplit:
# 			lowerWord = word.lower()
# 			if not lowerWord in stopwords:
# 				# wordList.append(lowerWord)
# 				vocab.append(lowerWord)
# 				srVocab.append(lowerWord)
# 				titleVocab.append(lowerWord)
# 				titleList.append(lowerWord)
# 			totalWords += 1
# 			try:
# 				val = float(word)
# 				totalNumbers += 1
# 			except ValueError:
# 				if word == word.upper() and word != word.lower():
# 					capsLock += 1
# 				pass
# 		# Check for link
# 		if body.lower().find("http") >= 0 or body.lower().find("www.") >= 0 or body.lower().find(".com") >= 0:
# 			featureVector[6] = 1

# 		# Count newlines
# 		numNewlines = body.count('\n')
# 		featureVector[4] = numNewlines
# 		# print "submission"
# 	# elif post.tag == "Comment":
# 	# 	# if featureVector[0] == 0:
# 	# 	# 	featureVector[0] = 1
# 	# 	print "comment"
# 	# elif post.tag == "Reply":
# 	# 	# if featureVector[0] < post.depth + 1:
# 	# 	# 	featureVector[0] = post.depth + 1
# 	# 	print "reply"
# 	else:
# 		body = post.attrib["body"]
# 		bodyList = re.findall(r"[0-9]+[.][0-9]+|[0-9,]+[.][0-9]+|[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+", body)
	
# 		# print "other"
# 	# Count number of numbers
# 	for word in bodyList:
# 		lowerWord = word.lower()
# 		if not lowerWord in stopwords:
# 			if post.tag == "Submission":
# 				wordList.append(lowerWord)
# 			vocab.append(lowerWord)
# 			srVocab.append(lowerWord)
# 		totalWords += 1
# 		try:
# 			val = float(word)

# 			totalNumbers += 1
# 		except ValueError:
# 			if word == word.upper() and word != word.lower():
# 				capsLock += 1
# 			pass

# 	for child in post:
# 		# Double chekc this
# 		totalNumbers, capsLock, totalWords = generateFeatures(child, featureVector, titleList, wordList, srVocab, totalNumbers, capsLock, totalWords)

# 	if post.tag == "Submission":
# 		if totalWords != 0:
# 			portionNumbers = float(totalNumbers) / totalWords
# 			# print totalNumbers
# 			# print totalWords
# 			portionCapsLock = float(capsLock) / totalWords
# 			# print capsLock
# 		else:
# 			portionNumbers = 0
# 			portionCapsLock = 0
# 		featureVector[5] = portionNumbers
# 		featureVector[7] = portionCapsLock


# 	return totalNumbers, capsLock, totalWords
# 	# for child in post:
# # Make a vector containing all words in each post
# # have it match up to the corresponding feature vector
# # append more slots for vocab after all are generated
# # fill in vocab slots

# print "Starting feature generation part 1"
# print datetime.datetime.now().time()
# # featureVector = [0]
# # list of lists
# listOfWords = []
# listOfTitles = []
# featureVectors = []
# nFold = []
# for file in fileList:
# 	if file[-1] == "\n":
# 		file = file[:-1]
# 	tree = ET.parse(file)
# 	root = tree.getroot()
# 	# count = 0

# 	# root is a subreddit
# 	for child in root:
# 		subredditVocab.append([])
# 		srVocab = subredditVocab[-1]
# 		featureVector = [0]*10 # TODO: make right size
# 		listOfWords.append([])
# 		wordList = listOfWords[-1]
# 		listOfTitles.append([])
# 		titleList = listOfTitles[-1]
# 		generateFeatures(child, featureVector, titleList, wordList, srVocab)
# 		featureVectors.append(featureVector)
# 		nFold.append(root.attrib["title"])
		# if count == 5:
		# 	break
		# count += 1
# print "Beginning vocab reduction"
# for srVocab in subredditVocab:
# 	srVocabCount = Counter(srVocab)
    # query_words = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in Set(query).difference(stopwords)]

# TODO: change it so that vocab is based on the folds
# probably rather than construct vocab, just use the above stuff to the word and title vecotrs i'm already getting
# then inside an n fold loop, construct the vocab
# MAYBE


# print "Starting feature generation part 2"
# print datetime.datetime.now().time()
# # titleVocab = sorted(set(titleVocab))
# # vocab = sorted(set(vocab))
# vocabDict = {}
# titleDict = {}
# for index, word in enumerate(vocab):
# 	vocabDict[word] = index
# for index, word in enumerate(titleVocab):
# 	titleDict[word] = index

# print len(vocab)
# print len(titleVocab)
# for index, featureVector in enumerate(featureVectors):
# 	words = listOfWords[index]
# 	title = listOfTitles[index]
# 	titleVector = [0] * len(titleVocab)
# 	vocabVector = [0] * len(vocab)
# 	for word in words:
# 		try:
# 			i = vocabDict[word]
# 			if i >= 0:
# 				# print i
# 				vocabVector[i] += 1
# 		except ValueError:
# 			pass
# 	for word in title:
# 		try:
# 			j = titleDict[word]
# 			if j >= 0:
# 				# print j
# 				titleVector[j] += 1
# 		except ValueError:
# 			pass
# 	featureVectors[index] = featureVector + titleVector + vocabVector
from featureGen2 import addVocabToVectors
outputName = ""
if len(sys.argv) > 1:
	outputName = sys.argv[1]
featureVectors = addVocabToVectors(outputName)
nFoldFile = open("Data/nFold" + outputName, "r")
nFold = nFoldFile.readline().split()
print len(featureVectors[3])
print "Feature generation complete"
print datetime.datetime.now().time()
# print featureVectors[0]
print len(featureVectors)
print len(nFold)
average = 0
skf = StratifiedKFold(nFold, 4)
for train,test in skf:
	total = 0
	correct = 0
	decisionTree = DecisionTreeClassifier(random_state=0)
	trainInput = [featureVectors[i] for i in train]
	trainOutput = [nFold[i] for i in train]
	testInput = [featureVectors[i] for i in test]
	testOutput = [nFold[i] for i in test]
	print "Train decision tree"
	print datetime.datetime.now().time()
	decisionTree.fit(trainInput, trainOutput)
	print "Training complete"
	print datetime.datetime.now().time()
	predictions = decisionTree.predict(testInput)
	for index, prediction in enumerate(predictions):
		# print "predict " + prediction
		# print testOutput[index]
		if prediction == testOutput[index]:
			correct += 1
		total += 1
	print "Fold result: "
	print "Correct: " + str(correct)
	print "Total: " + str(total)
	print "Accuracy: " + str(float(correct)/total) + "\n"
	average += float(correct)/total
average /= 4
print "Average: " + str(average)

# inLines = inFile.readlines()
# print "start"
# tree = ET.parse(sys.argv[1])
# root = tree.getroot()
# print root

# thing = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# thing2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
# thing3 = ["hi", "hi", "hi", "hi", "bye", "bye", "bye", "john", "john", "john", "john"]
# skf = StratifiedKFold(thing3, 3)
# for train,test in skf:
# 	print str(train) + str(test)
