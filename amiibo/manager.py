# coding=utf-8
import datetime
import json
import copy

from last_updated import LastUpdated
from .amiibo import Amiibo, AmiiboReleaseDates, AmiiboSeries, AmiiboType, Character, GameSeries
from .filterable import AmiiboCollection, FilterableCollection


class AmiiboManager:
    amiibos = AmiiboCollection()
    amiibosfull = AmiiboCollection()
    amiibosfullwithoutusage = AmiiboCollection()
    game_series = FilterableCollection()
    characters = FilterableCollection()
    types = FilterableCollection()
    amiibo_series = FilterableCollection()
    last_updated = None

    def __init__(self):
        if AmiiboManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.from_json()
            AmiiboManager.__instance = self

    __instance = None
    @staticmethod 
    def getInstance():
        if AmiiboManager.__instance == None:
            AmiiboManager()
        return AmiiboManager.__instance

    def to_json(self, file='database/amiibo.json'):
        data = {
            'amiibos': {
                str(amiibo.id): {
                    'name': amiibo.name,
                    'release': {
                        'na': amiibo.release.na.isoformat() if amiibo.release.na else None,
                        'jp': amiibo.release.jp.isoformat() if amiibo.release.jp else None,
                        'eu': amiibo.release.eu.isoformat() if amiibo.release.eu else None,
                        'au': amiibo.release.au.isoformat() if amiibo.release.au else None,
                    },
                    'games3DS': amiibo.games3DS,
                    'gamesWiiU': amiibo.gamesWiiU,
                    'gamesSwitch': amiibo.gamesSwitch
                }
                for amiibo in self.amiibosfull
            },
            'game_series': {
                str(game_series.id): game_series.name
                for game_series in self.game_series
            },
            'characters': {
                str(character.id): character.name
                for character in self.characters
            },
            'types': {
                str(type_.id): type_.name
                for type_ in self.types
            },
            'amiibo_series': {
                str(amiibo_series.id): amiibo_series.name
                for amiibo_series in self.amiibo_series
            },
        }

        with open(file, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    @classmethod
    def from_json(self, file='database/amiibo.json', file1='database/games_info.json'):
        with open(file, 'r', encoding="utf8") as f:
            data = json.load(f)
        with open(file1, 'r', encoding="utf-8-sig") as g:
            data1 = json.load(g)

        self.amiibosfull.update(
                Amiibo(self, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=AmiiboManager._parse_date(amiibo['release']['na']),
                        jp=AmiiboManager._parse_date(amiibo['release']['jp']),
                        eu=AmiiboManager._parse_date(amiibo['release']['eu']),
                        au=AmiiboManager._parse_date(amiibo['release']['au']),
                ), data1['amiibos'][id_]['games3DS'], data1['amiibos'][id_]['gamesWiiU'], data1['amiibos'][id_]['gamesSwitch'])
                for id_, amiibo in data['amiibos'].items()
        )

        self.amiibosfullwithoutusage.update(
                Amiibo(self, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=AmiiboManager._parse_date(amiibo['release']['na']),
                        jp=AmiiboManager._parse_date(amiibo['release']['jp']),
                        eu=AmiiboManager._parse_date(amiibo['release']['eu']),
                        au=AmiiboManager._parse_date(amiibo['release']['au']),
                ), data1['amiibos'][id_]['games3DS'], data1['amiibos'][id_]['gamesWiiU'], data1['amiibos'][id_]['gamesSwitch'])
                for id_, amiibo in data['amiibos'].items()
        )
        for amiibo in self.amiibosfullwithoutusage:
            amiibo.gamesSwitch = copy.deepcopy(amiibo.gamesSwitch)
            for game in amiibo.gamesSwitch:
                try:
                    del game['amiiboUsage']
                except:
                    pass
            amiibo.gamesWiiU = copy.deepcopy(amiibo.gamesWiiU)
            for game in amiibo.gamesWiiU:
                try:
                    del game['amiiboUsage']
                except:
                    pass
            amiibo.games3DS = copy.deepcopy(amiibo.games3DS)
            for game in amiibo.games3DS:
                try:
                    del game['amiiboUsage']
                except:
                    pass


        self.amiibos.update(
                Amiibo(self, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=self._parse_date(amiibo['release']['na']),
                        jp=self._parse_date(amiibo['release']['jp']),
                        eu=self._parse_date(amiibo['release']['eu']),
                        au=self._parse_date(amiibo['release']['au']),
                ), None, None, None) # TODO: add custom Amiibo class that doesn't need the games
                for id_, amiibo in data['amiibos'].items()
        )
        for amiibo in self.amiibos:
            try:
                del amiibo.gamesSwitch
                del amiibo.games3DS
                del amiibo.gamesWiiU
            except AttributeError:
                pass

        self.game_series.update(
                GameSeries(self, id_, name)
                for id_, name in data['game_series'].items()
        )
        self.characters.update(
                Character(self, id_, name)
                for id_, name in data['characters'].items()
        )
        self.types.update(
                AmiiboType(self, id_, name)
                for id_, name in data['types'].items()
        )
        self.amiibo_series.update(
                AmiiboSeries(self, id_, name)
                for id_, name in data['amiibo_series'].items()
        )
        self.last_updated = LastUpdated().read_timestamp()

    @staticmethod
    def _parse_date(value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None


if __name__ == "__main__":
    amiibo_manager = AmiiboManager.from_json()
    for amiibo_ in amiibo_manager.amiibos.sort(['amiibo_series_name', 'amiibo_type_id', 'game_series_name', 'character_name', 'variant_id']):
        print(amiibo_.name, amiibo_.game_series.name, amiibo_.character.name, amiibo_.amiibo_type.name, amiibo_.amiibo_series.name, amiibo_.variant_id >> 4 * 2)
    amiibo_manager.to_json()
