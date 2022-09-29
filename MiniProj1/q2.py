import gzip
import json
import matplotlib.pyplot as plt

emotionsGZIP = gzip.open("./goemotions.json.gz", "rb")
emotionsJSON = json.load(emotionsGZIP)

classification = {"positive" : 0, "negative" : 0, "ambiguous" : 0, "neutral" : 0}
emotion = {}