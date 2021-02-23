from model import getInputArgs, getIntentsData, getModel, bag_of_words
from pluginFactory import PluginFactory
from nltk.chat.util import Chat, reflections
import numpy
import random
import pickle

data = getIntentsData()

with open("data/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

model= getModel()
model.load("data/model.tflearn")

def chat(message):
        inp = message
        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        args= getInputArgs(data, tag, inp)
        plugin = PluginFactory.getPlugin(tag)
        if plugin!=None:
            return plugin.response(args)
        else:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            return random.choice(responses)

if __name__ == '__main__':
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        response= chat(inp)
        print(response)