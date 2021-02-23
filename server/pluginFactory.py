from plugins.time.plugin import PluginTime
from plugins.wikipedia.plugin import PluginWikipedia
from plugins.meteo.plugin import PluginMeteo
from plugins.trajet.plugin import PluginTrajet

class PluginFactory:

    def getPlugin(tag):
        if tag=="time":
            return PluginTime()
        elif tag=="meteo":
            return PluginMeteo()
        elif tag=="wikipedia":
            return PluginWikipedia()
        elif tag=="trajet":
            return PluginTrajet()

        return None
