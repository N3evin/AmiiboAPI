import datetime

from flask.json import JSONEncoder

from amiibo.amiibo import (Amiibo,
                           AmiiboReleaseDates,
                           AmiiboSeries,
                           AmiiboType,
                           Character,
                           GameSeries,
                           Hex)
from amiibo.filterable import FilterableCollection

class AmiiboJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Hex):
            return str(obj)
        elif isinstance(obj, FilterableCollection):
            return list(obj)
        elif isinstance(obj, Amiibo):
            returner = {
                'name': obj.name,
                'head': str(obj.head)[2:],
                'tail': str(obj.tail)[2:],
                'type': obj.amiibo_type.name if obj.amiibo_type else None,
                'gameSeries': obj.game_series.name if obj.game_series else None,
                'amiiboSeries': obj.amiibo_series.name if obj.amiibo_series else None,
                'character': obj.character.name if obj.character else None,
                'image': "https://raw.githubusercontent.com/N3evin/AmiiboAPI/master/images/icon_{}-{}.png".format(str(obj.head)[2:], str(obj.tail)[2:]),
                'release': obj.release
            }
            try:
                returner.update({'games3DS': obj.games3DS, 'gamesWiiU': obj.gamesWiiU, 'gamesSwitch': obj.gamesSwitch})
            except AttributeError:
                pass
            return returner
        elif isinstance(obj, (GameSeries, Character, AmiiboType, AmiiboSeries)):
            return {
                'key': obj.id,
                'name': obj.name,
            }
        elif isinstance(obj, AmiiboReleaseDates):
            return {
                'na': obj.na,
                'jp': obj.jp,
                'eu': obj.eu,
                'au': obj.au,
            }
        elif isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()

        return super().default(obj)