import requests 
import os
import re

class PluginWikipedia:

    def response(self, args=None):
        if args is not None:
            word= self.parseWord(args.group(1))
            return self.query(word)
        return "Je ne comprend pas la demande."

    def query(self, word):
        apiURL= "https://fr.wikipedia.org/api/rest_v1/page/summary/"
        response = requests.get(apiURL+word)
        data= response.json()
        if "extract" in data:
            return data["extract"]
        return "wikipedia n'as pas la réponse"

    def parseWord(self, word):
        x = word.title()
        tab= x.split()
        return "_".join(tab)