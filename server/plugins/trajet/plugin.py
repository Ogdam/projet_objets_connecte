import requests
import os
import re
import geocoder
from geopy.geocoders import Nominatim
import json

class PluginTrajet:

    def response(self, args=None):
        word = []
        if args is not None:
            word.append(self.parseWord(args.group(1)))
            word.append(self.parseWord(args.group(2)))
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
        word[0] = word[0].replace('_', ' ')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(word[0])
        dlat, dlng = location.latitude, location.longitude

        # get dist position
        word[1] = word[1].replace('_', ' ')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(word[1])
        elat, elng = location.latitude, location.longitude

        trajet = []
        try :
            e = "https://api.navitia.io/v1/coverage/fr-idf/journeys?key=88ede902-31c0-497b-a589-dff13c603a58&from={0}%3B{1}&to={2}%3B{3}&".format(
                dlng, dlat, elng, elat)
            r = requests.get(e)
            r = r.json()
            t = r['journeys'][0]
            trajet = self.makeReadableTransport(t)

            return json.dumps(trajet)
        except :
            return trajet


    def makeReadableTransport(self, transport):
        etape = []
        try :
            for sct in transport['sections']:
                section = {}
                if sct['type'] == "waiting":
                    continue
                elif  sct['type'] == "street_network":
                    section.update({'type' : 'walking'})
                    section.update({'path' : sct['path']})
                elif sct['type'] == "public_transport"  :
                    section.update({'type' : sct['display_informations']['physical_mode']})
                    section.update({'direction' : sct['display_informations']['direction']})
                    section.update({'label' : sct['display_informations']['label']})
                elif sct['type'] == 'transfer' :
                    section.update({'type' : 'tranfer'})
                    continue


                section.update({'from' : []})
                print(sct['type'])
                if sct['type'] == 'public_transport' :
                    print(1)
                    section['from'].append({'name' : sct['from']['name'], 'lat': sct['from']['stop_point']['coord']['lat'] , 'lng': sct['from']['stop_point']['coord']['lon']} )
                else :
                    print(2)
                    section['from'].append({'name' : sct['from']['name'], 'lat': sct['from']['address']['coord']['lat'] , 'lng': sct['from']['address']['coord']['lon']} )

                print(3)
                section.update({'to' : []})
                section['to'].append({'name' : sct['to']['name'], 'lat': sct['to']['stop_point']['coord']['lat'] , 'lng': sct['to']['stop_point']['coord']['lon']} )

                a = []
                a.append(section)
                etape.append(section)
        except Exception as e:
            print(e)
        return etape

    def getBestCarRoute(self, word):
        # get local position
        word[0] = word[0].replace('_', ' ')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(word[0])
        dlat, dlng = location.latitude, location.longitude

        # get dist position
        word[1] = word[1].replace('_', ' ')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(word[1])
        elat, elng = location.latitude, location.longitude

        trajet = []
        try :
            e = "https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey=dE3hg0qKh-fkPGqNWKgWIUE2KHNqfdyQHH6fJQJQX94&waypoint0=geo!{0},{1}&waypoint1=geo!{2},{3}&mode=fastest;car;traffic:disabled&language=fr-fr".format(dlat, dlng, elat, elng)
            r = requests.get(e)
            r = r.json()
            #t = r['journeys'][0]
            #trajet = self.makeReadableTransport(t)

            #return json.dumps(trajet)
            return r
        except :
            return trajet
