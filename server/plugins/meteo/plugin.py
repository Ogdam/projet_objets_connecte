import json
import requests 
import os

class PluginMeteo:
    def __init__(self):
        with open(os.path.abspath(os.path.dirname(__file__))+"\config.json") as file:
            config = json.load(file)
        self.access_key= config["access_key"]
        self.city= config["city"]
        self.apiURL= "http://api.weatherstack.com/current?"

    def response(self, args=None):
       response = requests.get(self.apiURL+"access_key="+self.access_key+"&query="+self.city)
       data= response.json()
       result = "Voici les infos meteo:\n"
       result += "temperature:    "+str(data["current"]["temperature"])+"\n"
       result += "weather_descriptions: "+" ".join(data["current"]["weather_descriptions"])+"\n"
       result += "wind_speed:   "+str(data["current"]["wind_speed"])+"\n"
       result += "pressure: "+str(data["current"]["pressure"])+"\n"
       result += "precip:   "+str(data["current"]["precip"])+"\n"
       result += "humidity: "+str(data["current"]["humidity"])+"\n"
       result += "visibility:   "+str(data["current"]["visibility"])+"\n"
       return result