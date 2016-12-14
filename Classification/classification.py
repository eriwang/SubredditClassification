# Brian Ma
# briandma

import sys
import operator
import math
import string
import re
import xml.etree.ElementTree as ET
from sklearn.tree import DecisionTreeClassifier, export_graphviz
# from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn import tree
import datetime
from collections import Counter
from featureGen2 import addVocabToVectors
import pickle

outputName = ""
oneHotAsBool = False
demo = False
if len(sys.argv) > 1:
	outputName = sys.argv[1]
	if len(sys.argv) > 2:
		oneHotAsBool = sys.argv[2]
		if len(sys.argv) > 3:
			demo = sys.argv[3]

# Finish making feature vectors
featureVectors = addVocabToVectors(outputName, oneHotAsBool)

nFoldFile = open("Data/" + outputName + "/nFold", "r")
nFold = nFoldFile.readline().split()


if demo == True:
	clf = DecisionTreeClassifier()
	clf.fit(featureVectors, nFold)
	export_graphviz(clf)
	# s = pickle.dump(clf, open(saveTree, "wb"))
	vocabFile = open("Data/" + outputName + "/vocab" , "r")
	titleVocabFile = open("Data/" + outputName + "/titleVocab" , "r")
	titleVocab = titleVocabFile.readline().split()
	vocab = vocabFile.readline().split()

	regexStr = "[0-9]+[0-9,]+[.][0-9]+|[0-9]+[.][0-9]+|[0-9]+[0-9,]+[0-9]|[\w]+['][\w]+|[\w]+"
	vocabDict = {}
	titleDict = {}
	for index, word in enumerate(vocab):
		vocabDict[word] = index
	for index, word in enumerate(titleVocab):
		titleDict[word] = index

	while(1):
		title = raw_input("Enter post title: ")
		body = raw_input("Enter the post: ")
		
		titleList =  re.findall(r"" + regexStr, title)
		bodyList =  re.findall(r"" + regexStr, body)

		featureVector = [0]*4
		featureVector[0] = len(titleList)
		featureVector[1] = len(title)
		featureVector[2] = len(bodyList)



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
		result = clf.predict([featureVector])
		print "\nPredicted subreddit: " + result[0] + "\n"
else:
	
	if oneHotAsBool:
		out = open("Results/oneHotAsBool_" + outputName, "w")
		
	else:
		out = open("Results/" + outputName, "w")
	print len(featureVectors)
	print len(nFold)
	average = 0
	skf = StratifiedKFold(nFold, 4)
	# NFold validation
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
			if prediction == testOutput[index]:
				correct += 1
			total += 1
		out.write("Fold result: \n")
		out.write("Correct: " + str(correct) + "\n")
		out.write("Total: " + str(total) + "\n")
		out.write("Accuracy: " + str(float(correct)/total) + "\n\n")
		average += float(correct)/total
		
	average /= 4
	out.write("Average: " + str(average))

