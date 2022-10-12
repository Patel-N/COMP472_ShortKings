from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import gzip
import json
import matplotlib.pyplot as plt

emotionsGZIP = gzip.open("./goemotions.json.gz", "rb")
emotionsJSON = json.load(emotionsGZIP)

#https://www.kaggle.com/code/catris25/multinomial-naive-bayes-with-countvectorizer
classification = {"positive" : 0, "negative" : 0, "ambiguous" : 0, "neutral" : 0}
emotions = {}
comments = []

def defineVocabulary(comments, classification, emotions):    
    X1_train, X1_test, y1_train, y1_test = train_test_split(comments, classification, test_size=0.2, random_state=0)
    # X2_train, X2_test, y2_train, y2_test = train_test_split(comments, emotions, test_size=0.2, random_state=0)
    vectorizer = CountVectorizer()    
    v  = vectorizer.fit(comments)
    print("Vocabulary size: ", len(v.vocabulary_))

    X1_train = vectorizer.fit_transform(X1_train)
    X1_test = vectorizer.transform(X1_test)

    BaseMNB(X1_train, X1_test, y1_train)
    
def BaseMNB(X1_train, X1_test, y1_train):
    classifier = MultinomialNB()
    # model2 = classifier.fit(X2_train, y2_train)
    classifier.fit(X1_train,y1_train)
    model1_prediction = classifier.predict(X1_test)
    print('Predicted class = ', model1_prediction)


def run(comments, classification, emotions):
    
    defineVocabulary(comments, classification, emotions)
    
