import sqlite3
import datetime
import json
import os

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


class AmiiboManager():
    def __init__(self):
        self.amiibos = AmiiboCollection()
        self.game_series = FilterableCollection()
        self.characters = FilterableCollection()
        self.types = FilterableCollection()
        self.amiibo_series = FilterableCollection()

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


    def to_db(self, db='database/amiibo.db'):
        if os.path.exists(db):
            os.remove(db)

        conn = sqlite3.connect(db)
        c = conn.cursor()

        c.execute(
            """
            CREATE TABLE amiibos (
                head INTEGER NOT NULL,
                tail INTEGER NOT NULL,
                name TEXT NOT NULL,
                release_na TEXT,
                release_jp TEXT,
                release_eu TEXT,
                release_au TEXT,
                PRIMARY KEY(head, tail)
            )
            """
        )

        c.execute(
            """
            CREATE TABLE game_series (
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                PRIMARY KEY(id)
            )
            """
        )

        c.execute(
            """
            CREATE TABLE characters (
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                PRIMARY KEY(id)
            )
            """
        )

        c.execute(
            """
            CREATE TABLE types (
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                PRIMARY KEY(id)
            )
            """
        )

        c.execute(
            """
            CREATE TABLE amiibo_series (
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                PRIMARY KEY(id)
            )
            """
        )

        c.execute(
            """
            CREATE VIEW amiibo_info AS
            SELECT
                amiibos.head,
                amiibos.tail,
                PRINTF('%08X', amiibos.head) AS head_hex,
                PRINTF('%08X', amiibos.tail) AS tail_hex,
                amiibos.name,
                amiibo_series.id AS amiibo_series_id,
                PRINTF('%02X', amiibo_series.id >> 4 * 2) AS amiibo_series_hex,
                amiibo_series.name AS amiibo_series,
                game_series.id AS game_series_id,
                PRINTF('%03X', game_series.id >> 4 * 5) AS game_series_hex,
                game_series.name AS game_series,
                characters.id AS character_id,
                PRINTF('%04X', characters.id >> 4 * 4) AS character_hex,
                characters.name AS character,
                amiibos.head & {variant:#010x} AS variant_id,
                PRINTF('%06X', amiibos.head & {variant:#010x} >> 4 * 2) AS variant_hex,
                types.id AS type_id,
                PRINTF('%02X', types.id >> 4 * 0) AS type_hex,
                types.name AS type,
                amiibos.release_na,
                amiibos.release_jp,
                amiibos.release_eu,
                amiibos.release_au
            FROM amiibos

            LEFT JOIN game_series
                ON (amiibos.head & {game_series:#010x}) = game_series.id

            LEFT JOIN characters
                ON (amiibos.head & {character:#010x}) = characters.id

            LEFT JOIN types
                ON (amiibos.head & {amiibo_type:#010x}) = types.id

            LEFT JOIN amiibo_series
                ON (amiibos.tail & {amiibo_series:#010x}) = amiibo_series.id

            ORDER BY
                amiibo_series.name,
                types.id,
                game_series.name,
                characters.name,
                amiibos.head & {variant:#010x}
            """
            .format(
                game_series=GAME_SERIES_MASK,
                character=CHARACTER_MASK,
                variant=VARIANT_MASK,
                amiibo_type=AMIIBO_TYPE_MASK,
                amiibo_series=AMIIBO_SERIES_MASK,
            )
        )

        c.executemany(
            """
            INSERT INTO amiibos (head, tail, name, release_na, release_jp, release_eu, release_au)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (amiibo.head.value, amiibo.tail.value, amiibo.name, amiibo.release.na, amiibo.release.jp, amiibo.release.eu, amiibo.release.au)
                for amiibo in self.amiibos
            ]
        )

        c.executemany(
            """
            INSERT INTO game_series (id, name)
            VALUES (?, ?)
            """,
            [
                (game_series.id.value, game_series.name)
                for game_series in self.game_series
            ]
        )

        c.executemany(
            """
            INSERT INTO characters (id, name)
            VALUES (?, ?)
            """,
            [
                (character.id.value, character.name)
                for character in self.characters
            ]
        )

        c.executemany(
            """
            INSERT INTO types (id, name)
            VALUES (?, ?)
            """,
            [
                (type_.id.value, type_.name)
                for type_ in self.types
            ]
        )

        c.executemany(
            """
            INSERT INTO amiibo_series (id, name)
            VALUES (?, ?)
            """,
            [
                (amiibo_series.id.value, amiibo_series.name)
                for amiibo_series in self.amiibo_series
            ]
        )

        conn.commit()
        conn.close()

    @classmethod
    def from_db(cls, db='database/amiibo.db'):
        conn = sqlite3.connect(db)
        c = conn.cursor()

        manager = cls()
        manager.amiibos.update(
            Amiibo(manager, *amiibo)
            for amiibo in cls._list_amiibos(c)
        )
        manager.game_series.update(
            GameSeries(manager, id_, name)
            for id_, name in cls._list_amiibo_knp(c, "game_series")
        )
        manager.characters.update(
            Character(manager, id_, name)
            for id_, name in cls._list_amiibo_knp(c, "characters")
        )
        manager.types.update(
            AmiiboType(manager, id_, name)
            for id_, name in cls._list_amiibo_knp(c, "types")
        )
        manager.amiibo_series.update(
            AmiiboSeries(manager, id_, name)
            for id_, name in cls._list_amiibo_knp(c, "amiibo_series")
        )

        conn.close()

        return manager

    @classmethod
    def _list_amiibos(cls, c):
        return (
            (row[0], row[1], row[2], AmiiboReleaseDates(
                na=cls._parse_date(row[3]),
                jp=cls._parse_date(row[4]),
                eu=cls._parse_date(row[5]),
                au=cls._parse_date(row[6]),
            ))
            for row in c.execute(
                """
                SELECT head, tail, name, release_na, release_jp, release_eu, release_au
                FROM amiibos
                ORDER BY head, tail
                """
            )
        )

    @classmethod
    def _list_amiibo_knp(cls, c, table_name):
        return (
            (row[0], row[1])
            for row in c.execute(
                """
                SELECT id, name
                FROM {}
                ORDER BY id
                """
                .format(table_name)
            )
        )

    @classmethod
    def _parse_date(cls, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None

    @classmethod
    def from_old_db(cls, db='database/database.db'):
        conn = sqlite3.connect(db)
        c = conn.cursor()

        manager = cls()
        manager.amiibos.update(
            Amiibo(manager, *amiibo)
            for amiibo in cls._list_amiibos_old(c)
        )
        manager.game_series.update(
            # In the db game series is stored as 12bits (0xFFF) but it should only be 10 bits (0xFFC)
            GameSeries(manager, id_, name)
            for id_, name in cls._list_amiibo_knp_old(c, "gameSeries")
        )
        manager.characters.update(
            Character(manager, id_, name)
            for id_, name in cls._list_amiibo_knp_old(c, "character")
        )
        manager.types.update(
            AmiiboType(manager, id_, name)
            for id_, name in cls._list_amiibo_knp_old(c, "type")
        )
        manager.amiibo_series.update(
            AmiiboSeries(manager, id_, name)
            for id_, name in cls._list_amiibo_knp_old(c, "amiiboSeries")
        )

        conn.close()

        return manager

    @classmethod
    def _list_amiibos_old(cls, c):
        return (
            (row[0], row[1], row[2], AmiiboReleaseDates(
                na=cls._parse_date(row[3]),
                jp=cls._parse_date(row[4]),
                eu=cls._parse_date(row[5]),
                au=cls._parse_date(row[6]),
            ))
            for row in c.execute(
                """
                SELECT
                    amiibo.head,
                    amiibo.tail,
                    amiibo.name,
                    releaseDate.northAmerica,
                    releaseDate.japan,
                    releaseDate.europe,
                    releaseDate.australia
                FROM amiibo

                LEFT JOIN releaseDate
                    ON releaseDate.id = (amiibo.head || amiibo.tail)

                ORDER BY amiibo.name
                """
            )
        )

    @classmethod
    def _list_amiibo_knp_old(cls, c, table_name):
        return (
            (row[0], row[1])
            for row in c.execute(
                """
                SELECT key, name
                FROM {}
                ORDER BY name
                """
                .format(table_name)
            )
        )

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

        return manager


if __name__ == "__main__":
    manager = AmiiboManager.from_json()
    for amiibo in manager.amiibos.sort(['amiibo_series_name', 'amiibo_type_id', 'game_series_name', 'character_name', 'variant_id']):
        print(amiibo.name, amiibo.game_series.name, amiibo.character.name, amiibo.amiibo_type.name, amiibo.amiibo_series.name, amiibo.variant_id >> 4 * 2)
    manager.to_json()
    manager.to_db()
