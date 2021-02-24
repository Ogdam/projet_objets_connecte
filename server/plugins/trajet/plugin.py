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
        return tranport

    def parseWord(self, word):
        x = word.title()
        tab= x.split()
        return "_".join(tab)

    def getPublicTransportBest(self, word):
        # get local position
        g = geocoder.ip('me')
        dlat, dlng = g.latlng

        # get dist position
        word = word.replace('_', ' ')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(word)
        elat, elng = location.latitude, location.longitude

        try :
            e = "https://api.navitia.io/v1/coverage/fr-idf/journeys?key=88ede902-31c0-497b-a589-dff13c603a58&from={0}%3B{1}&to={2}%3B{3}&".format(
                dlng, dlat, elng, elat)
            r = requests.get(e)
            r = r.json()

            trajet = r['journeys'][0]
            trajet = self.makeReadableTransport(trajet)

            return trajet
        except :
            return []


    def makeReadableTransport(self, transport):
        etape = []
        for sct in transport['sections']:
            section = {}
            if  sct['type'] == "street_network":
                section.update({'type' : 'walking'})
                section.update({'path' : sct['path']})
            elif sct['type'] == "public_transport"  :
                section.update({'type' : sct['display_informations']['physical_mode']})
                section.update({'direction' : sct['display_informations']['direction']})
                section.update({'label' : sct['display_informations']['label']})
            elif sct['type'] == 'transfer' :
                section.update({'type' : 'tranfer'})
            section.update({'from' : sct['from']['name']})
            section.update({'to' : sct['to']['name']})

            etape.append(section)

        return etape
