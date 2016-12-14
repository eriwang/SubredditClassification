from xml.etree.ElementTree import *
from helpers import * 
import praw


SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns', 'PoliticalDiscussion', 'LifeProTips', 'legaladvice', 'askphilosophy']


# Reddit Credentials
# u:EECS498Bot
# p:wangster
reddit = praw.Reddit(user_agent='Subreddit classification - data collection (by /u/EECS498Bot)', 
                     client_id='2eGzRj81THEygg', client_secret='uCtxG3tWHl4m9y5kiaGVZIi22ZI')


collectionStats = open('Collection Statistics.out', 'w')
totalSubmissions = 0

# Grabbing all available ~1000 submissions on each subreddit
for subredditTitle in SUBREDDITS:

    subredditWriter = open(subredditTitle + '.xml', 'w')
    print 'Gathering data for:', '/r/' + subredditTitle 

    subreddit = reddit.subreddit(subredditTitle)

    # Create basic tree
    root = Element('Subreddit', {'title':subredditTitle, 'display_name':subreddit.title})    
    submissions = {
        Element('Submission', {'id':submission.id, 'title':submission.title, 'upvotes':str(submission.ups), 
                               'downvotes':str(generate_downs(submission)), 'self_body':submission.selftext}
                ):submission for submission in subreddit.hot(limit=None)
        }
    root.extend(submissions.keys())

    print 'Expanding comments - This may take a while'
    # Add comment to each submission
    for xmlSub in submissions:
        submission = submissions[xmlSub]
        submission.comments.replace_more(limit=None)

        for comment in submission.comments:
            sub = SubElement(xmlSub, 'Comment', {'id':comment.id, 'upvotes':str(comment.ups), 'body':comment.body})
            generate_subs(sub, comment)

    subredditWriter.write(prettify(root).encode('utf-8'))
    subredditWriter.close()

    collectionStats.write('Found ' + str(len(submissions)) + ' submissions in /r/' + subredditTitle +  '\n')
    totalSubmissions += len(submissions)
    print 'Found', len(submissions), 'submissions in', subreddit.title, '\n'

collectionStats.write('\n' + 'Total Submissions collected: ' + str(totalSubmissions) + '\n')
collectionStats.close()

