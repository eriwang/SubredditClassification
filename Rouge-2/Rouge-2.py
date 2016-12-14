# REQUIRES PrettyTable to be installed
# pip install PrettyTable

from prettytable import PrettyTable
import xml.etree.ElementTree as ET
import numpy as np
import sys

SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns']

USERS = ['kaushik', 'brian', 'eric', 'daniel', 'moderator']
ALGOS = ['pagerank', 'tf-idf']

# Returns a ROUGE-2 score for the two summaries
def rouge2(prediction, annotation):
    predictionList = [x.lower() for x in prediction.split()]
    annotationList = [x.lower() for x in annotation.split()]

    predictionDict = {(predictionList[i] + predictionList[i+1]):0 for i in range(len(predictionList) - 1)}
    annotationDict = {(annotationList[i] + annotationList[i+1]):0 for i in range(len(annotationList) - 1)}

    for i in range(len(predictionList) - 1):
        predictionDict[predictionList[i] + predictionList[i+1]] += 1

    for i in range(len(annotationList) - 1):
        annotationDict[annotationList[i] + annotationList[i+1]] += 1
        
    predictionVector = []
    annotationVector = []
    for key in predictionDict.keys() + annotationDict.keys():
        predictionVector.append(0)
        annotationVector.append(0)

        if key in predictionDict:
            predictionVector[-1] = predictionDict[key]
        if key in annotationDict:
            annotationVector[-1] = annotationDict[key]
                       
    predictionVector = np.array(predictionVector)
    annotationvector = np.array(annotationVector)

    return float(np.dot(predictionVector, annotationVector))/ (np.linalg.norm(predictionVector) * np.linalg.norm(annotationVector))
    
results = {algo:{} for algo in ALGOS}
for algo in results:
    results[algo] = {subreddit:[] for subreddit in SUBREDDITS}

t = PrettyTable(['Algorithm', 'Annotation', 'SubReddit', 'Score'])
for algo in ALGOS:
    f = open(algo + '.annotations.xml', 'r')
    file = ET.fromstring(f.read())
    f.close()

    predicted = {}
    for subreddit in file.findall('Subreddit'):

        predicted[subreddit.attrib['title']] = subreddit.attrib['title'] + ' ' + subreddit.attrib['summary']
        
    for name in USERS:
        f = open(name + '.annotations.xml', 'r')
        file = ET.fromstring(f.read())
        f.close()
        
        annotated = {}
        for subreddit in file.findall('Subreddit'):
            
            annotated[subreddit.attrib['title']] = subreddit.attrib['title'] + ' '+  subreddit.attrib['summary']
            
            rouge = rouge2(predicted[subreddit.attrib['title']], annotated[subreddit.attrib['title']])
            t.add_row([algo, name, subreddit.attrib['title'], rouge])
            results[algo][subreddit.attrib['title']].append(rouge)

print t

stats = PrettyTable(['Algorithm', 'SubReddit', 'Mean', 'Median'])
for algo in results:
    for subreddit in SUBREDDITS:
        stats.add_row([algo, subreddit, np.mean(results[algo][subreddit]), np.median(results[algo][subreddit])])

print stats
