

import datetime

# titleVocab = sorted(set(titleVocab))
# vocab = sorted(set(vocab))
def addVocabToVectors(outputName, oneHotAsBool=False):
	vocabFile = open("Data/" + outputName + "/vocab" , "r")
	titleVocabFile = open("Data/" + outputName + "/titleVocab" , "r")
	featureVectorFile = open("Data/" + outputName + "/featureVectors1" , "r")
	listOfWordsFile = open("Data/" + outputName + "/listOfWords" , "r")
	listOfTitlesFile = open("Data/" + outputName + "/listOfTitles" , "r")
	
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
					if oneHotAsBool:
						vocabVector[i] = 1
					else:
						vocabVector[i] += 1
			except KeyError:
				pass
		for word in title:
			try:
				j = titleDict[word]
				if j >= 0:
					# print j
					if oneHotAsBool:
						titleVector[j] = 1
					else:
						titleVector[j] += 1
			except KeyError:
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