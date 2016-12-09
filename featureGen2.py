

import datetime

# titleVocab = sorted(set(titleVocab))
# vocab = sorted(set(vocab))
def addVocabToVectors(outputName):
	vocabFile = open("Data/vocab" + outputName, "r")
	titleVocabFile = open("Data/titleVocab" + outputName, "r")
	featureVectorFile = open("Data/featureVectors1" + outputName, "r")
	listOfWordsFile = open("Data/listOfWords" + outputName, "r")
	listOfTitlesFile = open("Data/listOfTitles" + outputName, "r")
	featureVectorFile2 = open("Data/featureVectors2" + outputName, "w")
	titleVocab = titleVocabFile.readline().split()
	vocab = vocabFile.readline().split()
	featureVectors = [line.split() for line in featureVectorFile]
	listOfWords = [line.split() for line in listOfWordsFile]
	listOfTitles = [line.split() for line in listOfTitlesFile]
	print "Starting feature generation part 2"
	print datetime.datetime.now().time()

	vocabDict = {}
	titleDict = {}
	for index, word in enumerate(vocab):
		vocabDict[word] = index
	for index, word in enumerate(titleVocab):
		titleDict[word] = index

	print len(vocab)
	print len(titleVocab)
	for index, featureVector in enumerate(featureVectors):
		words = listOfWords[index]
		title = listOfTitles[index]
		titleVector = [0] * len(titleVocab)
		vocabVector = [0] * len(vocab)
		for word in words:
			try:
				i = vocabDict[word]
				if i >= 0:
					# print i
					vocabVector[i] += 1
			except ValueError:
				pass
		for word in title:
			try:
				j = titleDict[word]
				if j >= 0:
					# print j
					titleVector[j] += 1
			except ValueError:
				pass
		featureVectors[index] = featureVector + titleVector + vocabVector
	print "Feature generation complete"
	print datetime.datetime.now().time()
	return featureVectors
	# for vec in featureVectors:
	# 	for word in vec:
	# 		featureVectorFile2.write(str(word) + " ")
	# 	featureVectorFile2.write("\n")
	# print "Features now in file"
	# print datetime.datetime.now().time()