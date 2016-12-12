from helpers import *
from xml.etree.ElementTree import *
import sys

SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns']

if len(sys.argv) < 2:
    print >> sys.stderr, 'ERROR: Inlcude name as command line argument'
    exit(1)

name = sys.argv[1].lower()

root = Element('Annotation', {'name':name})
for subreddit in SUBREDDITS:
    
    summary = raw_input('Summary for /r/' + subreddit + ': ')

    subXML = SubElement(root, 'Subreddit', {'title':subreddit, 'summary':summary})
    
w = open(name + '.annotations.xml', 'w')
w.write(prettify(root).encode('utf-8'))
