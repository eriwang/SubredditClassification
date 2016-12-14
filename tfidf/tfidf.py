
import sys
import pythonrouge
import xml.etree.ElementTree as ET
from summarizer import summarizer
from pythonrouge import pythonrouge

num_top = int(sys.argv[1])

subs = ['uofm', 'history', 'cscareerquestions', 'puns', 'engineering']

for sub in subs:
    # read sample data
    tree = ET.parse(sub + ".xml")
    root = tree.getroot()

    s = summarizer()

    summary = s.summarize(root, num_top)

    # get gold standard
    f = open('annotations/' + sub + '.txt')

    peer = summary
    model = f.read()

    print("summary:\n", peer)
    peer = peer.lower()
    model = model.lower()
    score = pythonrouge.pythonrouge(model, peer)
    print("R2 score:", score['ROUGE-2'], "R1 score:", score['ROUGE-1'])
