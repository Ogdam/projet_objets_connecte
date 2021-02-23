import requests
import os
import re
import geocoder
from geopy.geocoders import Nominatim

class PluginTrajet:

    def response(self, args=None):
        if args is not None:
            word= self.parseWord(args.group(1))
            return self.query(word)
        return "Je ne comprend pas la demande."

    def query(self, word):
        tranport = self.getPublicTransportBest(word)
        return "trajet"

    def parseWord(self, word):
        x = word.title()
        tab= x.split()
        return "_".join(tab)

    def getPublicTransportBest(self, word):
        g = geocoder.ip('me')
        dlat, dlong = g.latlng
        word = word.replace('_', ' ')
        address= word
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        elat, elong = location.latitude, location.longitude

        try :
            e = "https://api.navitia.io/v1/coverage/fr-idf/journeys?key=88ede902-31c0-497b-a589-dff13c603a58&from={0}%3B{1}&to={2}%3B{3}&".format(
                dlong, dlat, elong, elat)
            r = requests.get(e)
            r = r.json()
            trajet = r['journeys'][0]
            trajet.pop('calendars')
            return trajet
        except :
            return []
