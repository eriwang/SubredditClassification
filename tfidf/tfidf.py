
import sys
import xml.etree.ElementTree as ET
from summarizer import summarizer

num_top = int(sys.argv[1])

subs = ['uofm', 'history', 'cscareerquestions', 'puns', 'engineering']

for sub in subs:
    # read sample data
    tree = ET.parse(sub + ".xml")
    root = tree.getroot()

    s = summarizer()

    summary = s.summarize(root, num_top)

    print("summary:\n", summary)
