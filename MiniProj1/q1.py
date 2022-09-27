import gzip
import json
import matplotlib.pyplot as plt

emotionsGZIP = gzip.open("./goemotions.json.gz", "rb")
emotionsJSON = json.load(emotionsGZIP)

classification = {"positive" : 0, "negative" : 0, "ambiguous" : 0, "neutral" : 0}
emotion = {}

def updateClassification(classification, sentiment):
    sentimentCount = classification[sentiment] + 1
    classification[sentiment] = sentimentCount

def updateEmotion(emotion, feeling):
    if feeling not in emotion:
        emotion.update({feeling:1})
    else:
        emotionCount = emotion[feeling] + 1
        emotion[feeling] = emotionCount


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
    updateEmotion(emotion, value[1])
    updateClassification(classification, value[2])
    


def run():
    emotionPie = createPieChart(emotion, 'emotion')
    classificationPie = createPieChart(classification, 'classification')