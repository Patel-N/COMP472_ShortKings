import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.simplefilter("ignore") 

from matplotlib import test
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from collections import Counter

import json
import matplotlib.pyplot as plt
import gzip
import pandas as pd

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

def getBaseClassifiersPredictions(classifier, commentsTrainVector, commentsTestVector, classification_train, emotions_train):

    #emotions
    classifier.fit(commentsTrainVector, emotions_train)
    emotions_pred = classifier.predict(commentsTestVector)

    #classifications
    classifier.fit(commentsTrainVector, classification_train)
    classifications_pred = classifier.predict(commentsTestVector)

    return emotions_pred, classifications_pred

def getGridSearchWithModelAndParams(model, params, cvCount, iterations, commentsTrainVector, commentsTestVector, classification_train, emotions_train):
    tunedClassifier = GridSearchCV(model, params, cv=10, n_jobs=2)
    
    #emotions
    tunedClassifier.fit(commentsTrainVector, emotions_train)
    df = pd.DataFrame(tunedClassifier.cv_results_)
    
    emotions_pred = tunedClassifier.predict(commentsTestVector)
    
    print(df[['param_alpha', 'mean_test_score', 'rank_test_score']])
    print(tunedClassifier.best_score_)
    print(tunedClassifier.best_params_)
    print(tunedClassifier.predict(commentsTestVector))

    #classifications
    tunedClassifier.fit(commentsTrainVector, classification_train)
    df = pd.DataFrame(tunedClassifier.cv_results_)

    classifications_pred = tunedClassifier.predict(commentsTestVector)
    
    print(df[['param_alpha', 'mean_test_score', 'rank_test_score']])
    print(tunedClassifier.best_score_)
    print(tunedClassifier.best_params_)
    print(tunedClassifier.predict(commentsTestVector))

    return emotions_pred, classifications_pred

def run_q1():
    createPieChart(Counter(emotions), 'emotions_with_values')
    createPieChart(Counter(classification), 'classification_with_values')
    return comments, classification, emotions

def run_q2():
    #2.1
    getVocabulary()

    #2.2
    comments_train, comments_test, classification_train, classification_test, emotions_train, emotions_test = train_test_split(comments, classification, emotions, test_size=0.2, random_state=0)
    
    #2.3
    vectorizer = CountVectorizer()
    commentsTrainVector = vectorizer.fit_transform(comments_train)
    commentsTestVector = vectorizer.transform(comments_test)

    #2.3.1
    # getBaseClassifiersPredictions(MultinomialNB(), commentsTrainVector, commentsTestVector, classification_train, emotions_train)
    
    #2.3.2
    # getBaseClassifiersPredictions(DecisionTreeClassifier(), commentsTrainVector, commentsTestVector, classification_train, emotions_train)
    
    #2.3.3
    # getBaseClassifiersPredictions(MLPClassifier(), commentsTrainVector, commentsTestVector, classification_train, emotions_train)

    #2.3.4
    mnb_classifier = MultinomialNB()
    mnb_params = {'alpha': [0, 0.5, 1, 10]}
    # getGridSearchWithModelAndParams(mnb_classifier, mnb_params, 10, 2, commentsTrainVector, commentsTestVector, classification_train, emotions_train)
    
    #2.3.5
    dt_classifier = DecisionTreeClassifier()
    dt_params = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [800, 1000],
        'min_samples_split': [4, 8, 16]
    }
    getGridSearchWithModelAndParams(dt_classifier, dt_params, 10, 1, commentsTrainVector, commentsTestVector, classification_train, emotions_train)

def readData():
    for value in emotionsJSON:
        emotions.append(value[1])
        classification.append(value[2])
        comments.append(value[0])

#1.2
readData()
#1.3
# run_q1()
run_q2()