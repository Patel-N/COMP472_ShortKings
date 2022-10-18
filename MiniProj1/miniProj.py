from __future__ import print_function
from matplotlib import test
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

import json
import matplotlib.pyplot as plt
import gzip
import warnings
from collections import Counter

warnings.filterwarnings("ignore", category=DeprecationWarning) 

emotionsGZIP = gzip.open("./goemotions.json.gz", "rb")
emotionsJSON = json.load(emotionsGZIP)

classification = []
emotions = []
comments = []

def createPieChart(dict, dictName):
    labels = []
    values = []
    for x,y in dict.items():
        labels.append(x)
        values.append(y)
    plt.pie(values, labels=labels, autopct=lambda p:f'{p:.2f}%, {p*sum(values)/100 :.0f}')
    plt.savefig('./graphs/'+dictName)
    plt.clf()


def getVocabulary():
    vectorizer = CountVectorizer()
    X  = vectorizer.fit(comments)
    print("Vocabulary size: ", len(X.vocabulary_))

def baseMNB(commentsTrainVector, commentsTestVector, classification_train, classification_test, emotions_train, emotions_test):

    mnbClassifier = MultinomialNB()
    
    #emotions
    mnbClassifier.fit(commentsTrainVector, emotions_train)    
    emotions_pred = mnbClassifier.predict(commentsTestVector)

    #classifications
    mnbClassifier.fit(commentsTrainVector, classification_train)
    classification_pred = mnbClassifier.predict(commentsTestVector)
    
    return emotions_pred, classification_pred

def baseDT(commentsTrainVector, commentsTestVector, classification_train, classification_test, emotions_train, emotions_test):

    dtClassifier = DecisionTreeClassifier()

    #emotions
    dtClassifier.fit(commentsTrainVector, emotions_train)
    emotions_pred = dtClassifier.predict(commentsTestVector)
    print(emotions_pred)

    #classifications
    dtClassifier.fit(commentsTrainVector, classification_train)
    classification_pred = dtClassifier.predict(commentsTestVector)

    # for x,y in zip(classification_pred, emotions_pred):
    #     print(x + "\t\t" + y)

    return emotions_pred, classification_pred


def run_q1():
    createPieChart(Counter(emotions), 'emotions_2')
    createPieChart(Counter(classification), 'classification_2')
    return comments, classification, emotions

def run_q2(comments, classification, emotions):
    #2.1
    getVocabulary()


    #2.2
    comments_train, comments_test, classification_train, classification_test, emotions_train, emotions_test = train_test_split(comments, classification, emotions, test_size=0.2, random_state=0)
    
    #2.3
    vectorizer = CountVectorizer()
    commentsTrainVector = vectorizer.fit_transform(comments_train)
    commentsTestVector = vectorizer.transform(comments_test)

    #2.3.1
    baseMNB(commentsTrainVector, commentsTestVector, classification_train, classification_test, emotions_train, emotions_test)

    #2.3.2
    baseDT(commentsTrainVector, commentsTestVector, classification_train, classification_test, emotions_train, emotions_test)

for value in emotionsJSON:
    emotions.append(value[1])
    classification.append(value[2])
    comments.append(value[0])


comments, classification, emotions = run_q1()
run_q2(comments, classification, emotions)