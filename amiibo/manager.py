import sqlite3
import datetime
import json
import os
import hashlib

from .amiibo import (
    GAME_SERIES_MASK,
    CHARACTER_MASK,
    VARIANT_MASK,
    AMIIBO_TYPE_MASK,
    AMIIBO_SERIES_MASK,
    Amiibo,
    AmiiboReleaseDates,
    GameSeries,
    Character,
    AmiiboType,
    AmiiboSeries,
)
from .filterable import (
    AmiiboCollection,
    FilterableCollection,
)


class LastUpdated():
    def __init__(self, file='last-updated.json'):
        self.file = 'last-updated.json'

    def read(self):
        with open(self.file, 'r') as f:
            data = json.load(f)

        return {
            'sha1': data['sha1'],
            'timestamp': datetime.datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f"),
        }

    def write(self, sha1, timestamp):
        with open(self.file, 'w') as f:
            json.dump({
                'sha1': sha1,
                'timestamp': timestamp.isoformat(),
            }, f)

    def hash(self, data):
        value = json.dumps(data, sort_keys=True)
        return hashlib.sha1(value.encode('utf-8')).hexdigest()

    def __call__(self, data):
        sha1 = self.hash(data)
        try:
            last_update = self.read()
        except Exception as e:
            print(e)
            last_update = None

        if last_update is None or last_update['sha1'] != sha1:
            timestamp = datetime.datetime.utcnow()
            self.write(sha1, timestamp)
            print('Updated {}'.format(self.file))
            print('sha1: {}, timestamp: {}'.format(sha1, timestamp.isoformat()))
        else:
            timestamp = last_update['timestamp']

        return timestamp


class AmiiboManager():
    def __init__(self):
        self.amiibos = AmiiboCollection()
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
                }
                for amiibo in self.amiibos
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
    def from_json(cls, file='database/amiibo.json'):
        with open(file, 'r') as f:
            data = json.load(f)

        manager = cls()
        manager.amiibos.update(
            Amiibo(manager, id_[2:10], id_[10:18], amiibo['name'], AmiiboReleaseDates(
                na=cls._parse_date(amiibo['release']['na']),
                jp=cls._parse_date(amiibo['release']['jp']),
                eu=cls._parse_date(amiibo['release']['eu']),
                au=cls._parse_date(amiibo['release']['au']),
            ))
            for id_, amiibo in data['amiibos'].items()
        )
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
        manager.last_updated = LastUpdated()(data)

        return manager

    @classmethod
    def _parse_date(cls, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None


if __name__ == "__main__":
    manager = AmiiboManager.from_json()
    for amiibo in manager.amiibos.sort(['amiibo_series_name', 'amiibo_type_id', 'game_series_name', 'character_name', 'variant_id']):
        print(amiibo.name, amiibo.game_series.name, amiibo.character.name, amiibo.amiibo_type.name, amiibo.amiibo_series.name, amiibo.variant_id >> 4 * 2)
    manager.to_json()
    manager.to_db()
