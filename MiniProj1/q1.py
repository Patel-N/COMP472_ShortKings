import gzip
import json
import matplotlib.pyplot as plt

emotionsGZIP = gzip.open("./goemotions.json.gz", "rb")
emotionsJSON = json.load(emotionsGZIP)

classification = {"positive" : 0, "negative" : 0, "ambiguous" : 0, "neutral" : 0}
emotions = {}
comments = []

def updateClassification(classification, sentiment):
    sentimentCount = classification[sentiment] + 1
    classification[sentiment] = sentimentCount

def updateEmotion(emotions, feeling):
    if feeling not in emotions:
        emotions.update({feeling:1})
    else:
        emotionCount = emotions[feeling] + 1
        emotions[feeling] = emotionCount


def createPieChart(dict, dictName):
    labels = []
    values = []
    for x,y in dict.items():
        labels.append(x)
        values.append(y)
    plt.pie(values, labels=labels)
    plt.savefig('./graphs/'+dictName)
    plt.clf()

for value in emotionsJSON:
    updateEmotion(emotions, value[1])
    updateClassification(classification, value[2])
    comments.append(value[0])
    


def run():
    emotionPie = createPieChart(emotions, 'emotions')
    classificationPie = createPieChart(classification, 'classification')
    return comments, classification, emotions