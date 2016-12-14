from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown
import pickle
import nltk
import nltk.data
import numpy as np
import re
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
from nltk.corpus import stopwords
stop = stopwords.words('english')
# from nltk.corpus import stopwords
# stop = stopwords.words('english')

class summarizer:

    count_vect = ""
    tfidf = None

    def clean_document(self, document):
        # Remove all characters outside of Alpha Numeric
        # and some punctuation
        # document = re.sub('[^A-Za-z .-]+', ' ', document)
        document = document.replace('-', '')
        document = document.replace('...', '')
        document = document.replace('Mr.', 'Mr').replace('Mrs.', 'Mrs')
        document = ' '.join(document.split())
        return document

    def preprocess(self, document):
        document = document.replace('-', '')
        document = document.replace('.', '')
        return document

    def remove_stop_words(self, doc):
        doc = ' '.join([i for i in doc.split() if i not in stop])
        return doc

    def scoreDoc(self, doc):
        doc_freq_term = self.count_vect.transform([doc])
        self.doc_tfidf_matrix = self.tfidf.transform(doc_freq_term).todense().tolist()[0]

    def rank_sentences(self, doc, doc_matrix, feature_names,  top_n=1):
        sents = nltk.sent_tokenize(doc)
        print("Analyzing:", len(sents), "sentences")
        sentences = [nltk.word_tokenize(sent) for sent in sents]
        sentences = [[w for w in sent if nltk.pos_tag([w])[0][1] in NOUNS]
                      for sent in sentences]
        tfidf_sent = [[doc_matrix[feature_names.index(w.lower())]
                       for w in sent if w.lower() in feature_names]
                     for sent in sentences]

        # Calculate Sentence Values
        doc_val = sum(doc_matrix)
        sent_values = [sum(sent) / doc_val for sent in tfidf_sent]

        scored_sents = np.array(sent_values)

        # Apply Position Weights
        ranked_sents = [sent*(i/len(sent_values))
                    for i, sent in enumerate(sent_values)]

        ranked_sents = [pair for pair in zip(range(len(sent_values)), sent_values)]
        ranked_sents = sorted(ranked_sents, key=lambda x: x[1] *-1)
        # if len(ranked_sents) == 0:
        #     print("No Sentences")
        return ranked_sents[:top_n]

    def summarize(self, data, num_top):
        train_data = brown.words()
        doc = ""
        for post in data:
            d = post.attrib['self_body']
            doc += d

        # import corpus fron nltk
        # corpus = nltk.data.load('tokenizers/punkt/english.pickle')
        # [' '.join(document) for document in corpus]

        cleaned_document = self.clean_document(doc)
        doc = self.remove_stop_words(cleaned_document)

        # Fit and Transform the term frequencies into a vector
        count_vect = CountVectorizer()
        count_vect = count_vect.fit(train_data)
        freq_term_matrix = count_vect.transform(train_data)
        feature_names = count_vect.get_feature_names()

        # Fit and Transform the TfidfTransformer
        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)

        # Get the dense tf-idf matrix for the document
        story_freq_term_matrix = count_vect.transform([doc])
        story_tfidf_matrix = tfidf.transform(story_freq_term_matrix)
        story_dense = story_tfidf_matrix.todense()
        doc_matrix = story_dense.tolist()[0]

        # Get Top Ranking Sentences and join them as a summary
        top_sents = self.rank_sentences(doc, doc_matrix, feature_names, num_top)
        summary = '.'.join([cleaned_document.split('.')[i]
                            for i in [pair[0] for pair in top_sents]])
        summary = ' '.join(summary.split())
        print("Summary Sentances for: r/" + data.attrib['title'])
        return summary
