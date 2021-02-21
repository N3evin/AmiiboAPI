# coding=utf-8
import datetime
import json
import copy

from last_updated import LastUpdated
from .amiibo import Amiibo, AmiiboReleaseDates, AmiiboSeries, AmiiboType, Character, GameSeries
from .filterable import AmiiboCollection, FilterableCollection


class AmiiboManager:
    def __init__(self):
        self.amiibos = AmiiboCollection()
        self.amiibosfull = AmiiboCollection()
        self.amiibosfullwithoutusage = AmiiboCollection()
        self.game_series = FilterableCollection()
        self.characters = FilterableCollection()
        self.types = FilterableCollection()
        self.amiibo_series = FilterableCollection()
        self.last_updated = None

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
    def from_json(cls, file='database/amiibo.json', file1='database/games_info.json'):
        with open(file, 'r', encoding="utf8") as f:
            data = json.load(f)
        with open(file1, 'r', encoding="utf-8-sig") as g:
            data1 = json.load(g)
            
        manager = cls()
        manager.amiibosfull.update(
                Amiibo(manager, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=cls._parse_date(amiibo['release']['na']),
                        jp=cls._parse_date(amiibo['release']['jp']),
                        eu=cls._parse_date(amiibo['release']['eu']),
                        au=cls._parse_date(amiibo['release']['au']),
                ), data1['amiibos'][id_]['games3DS'], data1['amiibos'][id_]['gamesWiiU'], data1['amiibos'][id_]['gamesSwitch'])
                for id_, amiibo in data['amiibos'].items()
        )

        manager.amiibosfullwithoutusage.update(
                Amiibo(manager, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=cls._parse_date(amiibo['release']['na']),
                        jp=cls._parse_date(amiibo['release']['jp']),
                        eu=cls._parse_date(amiibo['release']['eu']),
                        au=cls._parse_date(amiibo['release']['au']),
                ), data1['amiibos'][id_]['games3DS'], data1['amiibos'][id_]['gamesWiiU'], data1['amiibos'][id_]['gamesSwitch'])
                for id_, amiibo in data['amiibos'].items()
        )
        for amiibo in manager.amiibosfullwithoutusage:
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


        manager.amiibos.update(
                Amiibo(manager, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                        na=cls._parse_date(amiibo['release']['na']),
                        jp=cls._parse_date(amiibo['release']['jp']),
                        eu=cls._parse_date(amiibo['release']['eu']),
                        au=cls._parse_date(amiibo['release']['au']),
                ), None, None, None) # TODO: add custom Amiibo class that doesn't need the games
                for id_, amiibo in data['amiibos'].items()
        )
        for amiibo in manager.amiibos:
            try:
                del amiibo.gamesSwitch
                del amiibo.games3DS
                del amiibo.gamesWiiU
            except AttributeError:
                pass

        manager.game_series.update(
                GameSeries(manager, id_, name)
                for id_, name in data['game_series'].items()
        )
        manager.characters.update(
                Character(manager, id_, name)
                for id_, name in data['characters'].items()
        )
        manager.types.update(
                AmiiboType(manager, id_, name)
                for id_, name in data['types'].items()
        )
        manager.amiibo_series.update(
                AmiiboSeries(manager, id_, name)
                for id_, name in data['amiibo_series'].items()
        )
        manager.last_updated = LastUpdated().read_timestamp()

        return manager

    @classmethod
    def _parse_date(cls, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None


if __name__ == "__main__":
    amiibo_manager = AmiiboManager.from_json()
    for amiibo_ in amiibo_manager.amiibos.sort(['amiibo_series_name', 'amiibo_type_id', 'game_series_name', 'character_name', 'variant_id']):
        print(amiibo_.name, amiibo_.game_series.name, amiibo_.character.name, amiibo_.amiibo_type.name, amiibo_.amiibo_series.name, amiibo_.variant_id >> 4 * 2)
    amiibo_manager.to_json()
