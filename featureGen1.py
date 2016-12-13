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
import os






# Open files
fileList = open(sys.argv[1], "r").readlines()
#test = open(sys.argv[2], "r")
# out = open(sys.argv[1] + ".out", "w")
outputName = ""
if len(sys.argv) > 2:
	outputName = sys.argv[2]

stopwordsFile = open("stopwords.txt", "r")
stopwords = [line[:-1] for line in stopwordsFile]

vocab = []
titleVocab = []
# subredditVocab = []

### Overall features
# One hot encoding for words ( % of words that are that word)
# Frequency of question marks [9] (% of tokens that are ?) (decreased accuracy)
# Frequency of punctuation [10] (% of tokens that are punct) (decreased accuracy)
# Average length of word (?) (redundant - length of post + # words in post)
# Capitalized after . or ? [11] (?)
# Number of sentences [8]

### Post features
# Words in title [end + 1]
# Number of words in title [0]
# Length of title [1]
# Words in post [end + 2]
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
# Deepest reply
# Number of comments
# Average number of words per comment / reply
# Portion of words that are numbers
# Number of words
# 

#Note: parse so that ....... is together which means .....? will also probalby be together
# Means instead of doing ==, gonna have to do find/in
# Parse string so that we keep numbers together and keep punctuation as tokens
# Includes .?
# regexStr = "[0-9]+[0-9,]+[.][0-9]+|[0-9]+[.][0-9]+|[0-9]+[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+|[.?]+"
# Doesn't include .?
regexStr = "[0-9]+[0-9,]+[.][0-9]+|[0-9]+[.][0-9]+|[0-9]+[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+"

def generateFeatures(post, featureVector, titleList, wordList, totalNumbers=0, capsLock=0, totalWords=0, numSentences=0, qMarkCount=0, numPunct=0):
	previousWasPunct = False
	numCaps = 0
	numPossibleCaps = 0
	# bodyList = body.split() # TODO make this regex from p4
	if post.tag == "Submission":
		body = post.attrib["self_body"]
		bodyList =  re.findall(r"" + regexStr, body)
		
		title = post.attrib["title"]
		titleSplit =  re.findall(r"" + regexStr, title)
		featureVector[0] = len(titleSplit)
		featureVector[1] = len(title)
		featureVector[2] = len(bodyList)
		featureVector[3] = len(body)

		for word in titleSplit:
			idx = word.find("?") 
			if idx >= 0 or word.find(".") >= 0:
				if idx >= 0:
					qMarkCount += 1
				numSentences += 1
				previousWasPunct = True
				# Uncomment if puncutation is removed from tokens
				# continue
			else:
				if previousWasPunct == True:
					numPossibleCaps += 1
					if word[0] >= 'A' and word[0] <= 'Z':
						numCaps += 1

					previousWasPunct = False
			# if not re.search('[\w]', word):
			# 	numPunct += 1
			# 	continue;
			

			lowerWord = word.lower()
			if not lowerWord in stopwords:
				# wordList.append(lowerWord)
				vocab.append(lowerWord)
				# srVocab.append(lowerWord)
				titleVocab.append(lowerWord)
				titleList.append(lowerWord)
			totalWords += 1
			try:
				val = float(word)
				totalNumbers += 1
			except ValueError:
				if word == word.upper() and word != word.lower():
					capsLock += 1
				pass
		# Check for link
		# if body.lower().find("http") >= 0 or body.lower().find("www.") >= 0 or body.lower().find(".com") >= 0:
		# 	featureVector[6] = 1

		# Count newlines
		numNewlines = body.count('\n')
		# featureVector[4] = numNewlines

	# else:
	# 	body = post.attrib["body"]
	# 	bodyList = re.findall(r"" + regexStr, body)
	
		# print "other"
		# Count number of numbers
	for word in bodyList:
		idx = word.find("?")
		if idx >= 0 or word.find(".") >= 0:
			if idx >= 0:
				qMarkCount += 1
			numSentences += 1
			previousWasPunct = True
			# Uncomment if puncutation is removed from tokens
			# continue
		else:
			if previousWasPunct == True:
				numPossibleCaps += 1
				if word[0] >= 'A' and word[0] <= 'Z':
					numCaps += 1
				previousWasPunct = False

		# if not re.search('[\w]', word):
		# 	numPunct += 1
		# 	continue

		lowerWord = word.lower()
		if not lowerWord in stopwords:
			# if post.tag == "Submission":
			wordList.append(lowerWord)
			vocab.append(lowerWord)
			# srVocab.append(lowerWord)
		totalWords += 1
		try:
			val = float(word)

			totalNumbers += 1
		except ValueError:
			if word == word.upper() and word != word.lower():
				capsLock += 1
			pass

	# for child in post:
	# 	# Double chekc this
	# 	totalNumbers, capsLock, totalWords, numSentences, qMarkCount, numPunct = generateFeatures(child, featureVector, titleList, wordList, totalNumbers, capsLock, totalWords, numSentences, qMarkCount, numPunct)

	if post.tag == "Submission":
		if totalWords != 0:
			portionNumbers = float(totalNumbers) / totalWords
			# print totalNumbers
			# print totalWords
			portionCapsLock = float(capsLock) / totalWords
			qMarkPercent = float(qMarkCount) / (qMarkCount + totalWords)
			percentPunct = float(numPunct) / totalWords
			# print capsLock
		else:
			portionNumbers = 0
			portionCapsLock = 0
			qMarkPercent = 0
			percentPunct = 0
		if numPossibleCaps != 0:
			percentCap = float(numCaps) / numPossibleCaps
		else:
			percentCap = 0
		featureVector[4] = portionNumbers
		# featureVector[7] = portionCapsLock
		# featureVector[8] = numSentences
		# featureVector[9] = qMarkPercent
		# featureVector[10] = percentPunct
		# featureVector[11] = percentCap


	return totalNumbers, capsLock, totalWords, numSentences, qMarkCount, numPunct
	# for child in post:
# Make a vector containing all words in each post
# have it match up to the corresponding feature vector
# append more slots for vocab after all are generated
# fill in vocab slots
if not os.path.exists("Data/" + outputName):
	os.makedirs("Data/" + outputName)
vocabFile = open("Data/" + outputName + "/vocab", "w")
titleVocabFile = open("Data/" + outputName + "/titleVocab" , "w")
featureVectorFile = open("Data/" + outputName + "/featureVectors1" , "w")
nFoldFile = open("Data/" + outputName + "/nFold" , "w")
listOfWordsFile = open("Data/" + outputName + "/listOfWords" , "w")
listOfTitlesFile = open("Data/" + outputName + "/listOfTitles" , "w")

print "Starting feature generation part 1"
print datetime.datetime.now().time()
# featureVector = [0]
# list of lists
listOfWords = []
listOfTitles = []
featureVectors = []
nFold = []
for file in fileList:
	if file[-1] == "\n":
		file = file[:-1]
	tree = ET.parse(file)
	root = tree.getroot()
	# count = 0

	# root is a subreddit
	for child in root:
		# subredditVocab.append([])
		# srVocab = subredditVocab[-1]
		featureVector = [0]*5 # TODO: make right size
		listOfWords.append([])
		wordList = listOfWords[-1]
		listOfTitles.append([])
		titleList = listOfTitles[-1]
		generateFeatures(child, featureVector, titleList, wordList)
		featureVectors.append(featureVector)
		nFold.append(root.attrib["title"])
		# if count == 5:
		# 	break
		# count += 1

titleVocab = sorted(set(titleVocab))
vocab = sorted(set(vocab))


for word in vocab:
	vocabFile.write(word + " ")
for word in titleVocab:
	titleVocabFile.write(word + " ")
for n in nFold:
	nFoldFile.write(n + " ")
for vec in featureVectors:
	for word in vec:
		featureVectorFile.write(str(word) + " ")
	featureVectorFile.write("\n")
for vec in listOfTitles:
	for word in vec:
		listOfTitlesFile.write(word + " ")
	listOfTitlesFile.write("\n")
for vec in listOfWords:
	for word in vec:
		listOfWordsFile.write(word + " ")
	listOfWordsFile.write("\n")

# for srVocab in subredditVocab:
# 	srVocabCount = Counter(srVocab)
    # query_words = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in Set(query).difference(stopwords)]

# TODO: change it so that vocab is based on the folds
# probably rather than construct vocab, just use the above stuff to the word and title vecotrs i'm already getting
# then inside an n fold loop, construct the vocab
# MAYBE


#Vocab
#titleVocab
#featureVectors
#listOfWords
#listOfTitles
#nFold

#subredditVocab?