from xml.etree.ElementTree import *
from helpers import * 
import praw


SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns']


# Reddit Credentials
# u:EECS498Bot
# p:wangster
reddit = praw.Reddit(user_agent='Subreddit classification - data collection (by /u/EECS498Bot)', 
                     client_id='2eGzRj81THEygg', client_secret='uCtxG3tWHl4m9y5kiaGVZIi22ZI')


collectionStats = open('Collection Statistics.txt.', 'w')
totalSubmissions = 0

# Grabbing all available ~1000 submissions on each subreddit
for subredditTitle in SUBREDDITS:

    subredditWriter = open(subredditTitle + '.xml', 'w')
    print 'Gathering data for:', '/r/' + subredditTitle 

    
    subreddit = reddit.subreddit(subredditTitle)
    numSubmissions = 0

    root = Element('Subreddit', {'title':subredditTitle, 'display_name':subreddit.title})
    
    submissions = {Element('Submission', {'id':submission.id, 'title':submission.title, 'upvotes':str(submission.ups)})
                   :submission for submission in subreddit.hot(limit=10)}
    root.extend(submissions.keys())

    for key in submissions:
        sub

    print prettify(root)

    for submission in subreddit.hot(limit=None):
        if submission.is_self or submission.is_self == False:
            submissions.append(Element('Submission'))
            submissions[-1].set('title', submission.title)
            

            numSubmissions += 1


    collectionStats.write('Found ' + str(numSubmissions) + ' submissions in /r/' + subredditTitle +  '\n')
    totalSubmissions += numSubmissions
    print 'Found', numSubmissions, 'submissions in', subreddit.title, '\n'

collectionStats.write('\n' + 'Total Submissions collected: ' + str(totalSubmissions) + '\n')
collectionStats.close()
