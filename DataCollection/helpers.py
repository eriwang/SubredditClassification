from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_downs(submission):
    ratio = submission.upvote_ratio
    ups = int(round((ratio*submission.score)/(2*ratio - 1)) if ratio != 0.5 else round(submission.score/2))
    downs = ups - submission.score
    return downs

def generate_subs(xmlSub, comment):
    for reply in comment.replies:
        sub = ElementTree.SubElement(xmlSub, 'Reply', {'id':reply.id, 'upvotes':str(reply.ups),'body':reply.body})
        generate_subs(sub, reply)
