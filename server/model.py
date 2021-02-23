import tflearn
import json
import pickle
from imutils import paths
import os
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import re

def getIntentsData():
    with open("intents.json") as file:
        data = json.load(file)

    #load plugins intents
    pluginsPaths = list(paths.list_files('plugins', validExts="json"))
    for (i, pluginPath) in enumerate(pluginsPaths):
        name = pluginPath.split(os.path.sep)[-2]
        filname = pluginPath.split(os.path.sep)[-1]
        if filname != "intents.json":
            continue
        print("loading ", name, pluginPath)
        with open(pluginPath) as pluginFile:
            dataPlugin= json.load(pluginFile)
        for intent in dataPlugin["intents"]:
            data["intents"].append(intent)
    print("nbrs intents --------------->",len( data["intents"]))
    return data

def getModel():
    with open("data/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    return model

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def getInputArgs(data, tag, input):
    for tg in data["intents"]:
        if tg['tag'] == tag:
            patterns = tg['patterns']
    for pat in patterns:
        match= re.search(pat, input)
        if match:
            return match
    return None
