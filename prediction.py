import pickle
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import sys
import re

pickleFile = sys.argv[1]
# pick = open(pickleFile, "rb")
decisionTree = pickle.load(pickleFile)

vocabFile = open("Data/forPrediction/vocab" , "r")
titleVocabFile = open("Data/forPrediction/titleVocab" , "r")
titleVocab = titleVocabFile.readline().split()
vocab = vocabFile.readline().split()

title = input("Enter post title: ")
body = input("Enter the post: ")
regexStr = "[0-9]+[0-9,]+[.][0-9]+|[0-9]+[.][0-9]+|[0-9]+[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+"
titleList =  re.findall(r"" + regexStr, title)
bodyList =  re.findall(r"" + regexStr, body)

featureVector = [0]*4
featureVector[0] = len(titleList)
featureVector[1] = len(title)
featureVector[2] = len(bodyList)



vocabDict = {}
titleDict = {}
for index, word in enumerate(vocab):
	vocabDict[word] = index
for index, word in enumerate(titleVocab):
	titleDict[word] = index


titleVector = [0] * len(titleVocab)
vocabVector = [0] * len(vocab)
totalNumbers = 0
for word in bodyList:
	try:
		val = float(word)
		totalNumbers += 1
	except ValueError:
		pass
	try:
		i = vocabDict[word]
		if i >= 0:
			# print i
			vocabVector[i] = 1
	except KeyError:
		pass
for word in titleList:
	try:
		val = float(word)
		totalNumbers += 1
	except ValueError:
		pass
	try:
		j = titleDict[word]
		if j >= 0:
			# print j
			titleVector[j] = 1
	except KeyError:
		pass

portionNumbers = float(totalNumbers) / (len(bodyList) + len(titleList))
featureVector[3] = portionNumbers
featureVector = featureVector + titleVector + vocabVector
result = decisionTree.predict(featureVector)
print result