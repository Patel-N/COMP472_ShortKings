from sklearn.feature_extraction.text import CountVectorizer
import sys
import numpy as np

def defineVocabulary(comments):

    vectorizer = CountVectorizer()
    X  = vectorizer.fit(comments)
    np.set_printoptions(threshold=sys.maxsize)
    # 2.1
    print("Vocabulary size: ", len(X.vocabulary_))

def run(comments, classification, emotions):
    defineVocabulary(comments)
