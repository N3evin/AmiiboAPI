# coding=utf-8
import collections
import copy
import datetime
import itertools


class Filterable:
    def __init__(self, func, key):
        self.func = func
        self.key = key

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def filterable(key):
    def wrapped(func):
        return Filterable(func, key)

    return wrapped


class Sortable:
    def __init__(self, func, key):
        self.func = func
        self.key = key

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def sortable(key):
    def wrapped(func):
        return Sortable(func, key)

    return wrapped


class FilterableCollectionMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Fetch all inherited properties from base -> current, replacing properties with the newest version
        all_attrs = dict(itertools.chain(*[base.__dict__.items() for base in bases] + [attrs.items()]))

        attrs['FILTERS'] = {
            value.key: value
            for value in all_attrs.values()
            if isinstance(value, Filterable)
        }
        attrs['SORTERS'] = {
            value.key: value
            for value in all_attrs.values()
            if isinstance(value, Sortable)
        }

        return type.__new__(mcs, name, bases, attrs)


class FilterableCollection(metaclass=FilterableCollectionMeta):
    def __init__(self, iterable=None):
        self._data = collections.OrderedDict()
        if iterable:
            self.update(iterable)

    def __iter__(self):
        yield from self._data.values()

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    def deepcopy(self):
        return copy.deepcopy(self)

    def add(self, value):
        self._data[value.id] = value

    def update(self, iterable):
        self._data.update((
            (v.id, v)
            for v in iterable
        ))

    def filter(self, **kwargs):
        filters = [
            self.FILTERS[key](self, value)
            for key, value in kwargs.items()
            if key in self.FILTERS
        ]
        if not filters:
            return self

        return self.__class__(
                value
                for value in self
                if all(f(value) for f in filters)
        )

    def sort(self, *args):
        sorts = [
            self.SORTERS[arg](self)
            for arg in args
            if arg in self.SORTERS
        ]
        if not sorts:
            return self

        return self.__class__(sorted(self, key=lambda x: tuple(f(x) for f in sorts)))

    @filterable('id')
    def filter_id(self, value):
        return lambda x: x.id == value

    @filterable('name')
    def filter_name(self, value):
        value = value.lower()
        return lambda x: value in x.name.lower()

    @sortable('id')
    def sort_id(self):
        return lambda x: x.id

    @sortable('name')
    def sort_name(self):
        return lambda x: x.name


class AmiiboCollection(FilterableCollection):
    @filterable('id')
    def filter_id(self, value):
        return lambda x: x.id == value

    @filterable('head')
    def filter_head(self, value):
        return lambda x: x.head == value

    @filterable('tail')
    def filter_tail(self, value):
        return lambda x: x.tail == value

    @filterable('game_series_id')
    def filter_game_series_id(self, value):
        return lambda x: x.game_series.id == value

    @filterable('game_series_name')
    def filter_game_series_name(self, value):
        value = value.lower() if value else value
        return lambda x: value in x.game_series.name.lower()

    @filterable('switch_titleid')
    def filter_switch_titleid(self, value):
        return lambda x: any(value in game.get("gameID") for game in x.gamesSwitch)

    @filterable('wiiu_titleid')
    def filter_wiiu_titleid(self, value):
        return lambda x: any(value in game.get("gameID") for game in x.gamesWiiU)

    @filterable('3ds_titleid')
    def filter_3ds_titleid(self, value):
        return lambda x: any(value in game.get("gameID") for game in x.games3DS)

    @filterable('character_id')
    def filter_character_id(self, value):
        return lambda x: x.character.id == value

    @filterable('character_name')
    def filter_character_name(self, value):
        value = value.lower() if value else value
        return lambda x: value in x.character.name.lower()

    @filterable('variant_id')
    def filter_variant_id(self, value):
        return lambda x: x.variant_id == value

    @filterable('amiibo_type_id')
    def filter_amiibo_type_id(self, value):
        return lambda x: x.amiibo_type.id == value

    @filterable('amiibo_type_name')
    def filter_amiibo_type_name(self, value):
        value = value.lower() if value else value
        return lambda x: x.amiibo_type.name.lower() == value

    @filterable('amiibo_model_id')
    def filter_amiibo_model_id(self, value):
        return lambda x: x.amiibo_model_id == value

    @filterable('amiibo_series_id')
    def filter_amiibo_series_id(self, value):
        return lambda x: x.amiibo_series.id == value

    @filterable('amiibo_series_name')
    def filter_amiibo_series_name(self, value):
        value = value.lower() if value else value
        return lambda x: value in x.amiibo_series.name.lower()

    @sortable('game_series_id')
    def sort_game_series_id(self):
        return lambda x: x.game_series.id

    @sortable('game_series_name')
    def sort_game_series_name(self):
        return lambda x: x.game_series.name

    @sortable('character_id')
    def sort_character_id(self):
        return lambda x: x.character.id

    @sortable('character_name')
    def sort_character_name(self):
        return lambda x: x.character.name

    @sortable('variant_id')
    def sort_variant_id(self):
        return lambda x: x.variant_id

    @sortable('amiibo_type_id')
    def sort_amiibo_type_id(self):
        return lambda x: x.amiibo_type.id

    @sortable('type_name')
    def sort_type_name(self):
        return lambda x: x.amiibo_type.name

    @sortable('amiibo_model_id')
    def sort_amiibo_model_id(self):
        return lambda x: x.amiibo_model_id

    @sortable('amiibo_series_id')
    def sort_amiibo_series_id(self):
        return lambda x: x.amiibo_series.id

    @sortable('amiibo_series_name')
    def sort_amiibo_series_name(self):
        return lambda x: x.amiibo_series.name

    @sortable('release_na')
    def sort_release_na(self):
        return lambda x: x.release.na or datetime.date.max

    @sortable('release_jp')
    def sort_release_jp(self):
        return lambda x: x.release.jp or datetime.date.max

    @sortable('release_eu')
    def sort_release_eu(self):
        return lambda x: x.release.eu or datetime.date.max

    @sortable('release_au')
    def sort_release_au(self):
        return lambda x: x.release.au or datetime.date.max
