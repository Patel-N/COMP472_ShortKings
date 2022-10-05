from sklearn.feature_extraction.text import CountVectorizer

def defineVocabulary(comments):
    vectorizer = CountVectorizer()
    X  = vectorizer.fit(comments)
    print("Vocabulary size: ", len(X.vocabulary_))

def run(comments, classification, emotions):
    defineVocabulary(comments)
