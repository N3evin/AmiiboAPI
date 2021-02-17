# coding=utf-8
from cached_property import cached_property

GAME_SERIES_MASK   = 0xFFF00000
CHARACTER_MASK     = 0xFFFF0000
VARIANT_MASK       = 0xFFFFFF00
AMIIBO_TYPE_MASK   = 0x000000FF
AMIIBO_MODEL_MASK  = 0XFFFF0000
AMIIBO_SERIES_MASK = 0x0000FF00
UNKNOWN_MASK       = 0x000000FF

AMIIBO_HEAD_BITSHIFT   = 4 * 8
AMIIBO_TAIL_BITSHIFT   = 4 * 0
GAME_SERIES_BITSHIFT   = 4 * 5
CHARACTER_BITSHIFT     = 4 * 4
VARIANT_BITSHIFT       = 4 * 2
AMIIBO_TYPE_BITSHIFT   = 4 * 0
AMIIBO_MODEL_BITSHIFT  = 4 * 4
AMIIBO_SERIES_BITSHIFT = 4 * 2
UNKNOWN_BITSHIFT       = 4 * 0


class Hex:
    length = 8
    bitshift = 0
    mask = 0xFFFFFFFF

    def __init__(self, value):
        self.value = self.to_int(value) & self.mask

    def __str__(self):
        return '{0:#0{1}x}'.format(self.value >> self.bitshift, 2 + self.length)

    def __hash__(self):
        return self.value

    def to_int(self, value):
        if type(value) is int:
            return value
        elif type(value) is str:
            return (int(value, 16) << self.bitshift) & self.mask
        elif isinstance(value, Hex):
            return value.value

        raise TypeError(value)

    def __and__(self, other):
        return self.value & self.to_int(other)

    def __or__(self, other):
        return self.value | self.to_int(other)

    def __eq__(self, other):
        return self.value == self.to_int(other)

    def __ne__(self, other):
        return self.value != self.to_int(other)

    def __lt__(self, other):
        return self.value < self.to_int(other)

    def __le__(self, other):
        return self.value <= self.to_int(other)

    def __gt__(self, other):
        return self.value > self.to_int(other)

    def __ge__(self, other):
        return self.value >= self.to_int(other)

    def __lshift__(self, other):
        return self.value << self.to_int(other)

    def __rshift__(self, other):
        return self.value >> self.to_int(other)

    def __add__(self, other):
        return self.value + self.to_int(other)

    def __sub__(self, other):
        return self.value - self.to_int(other)


class AmiiboHex(Hex):
    length = 16
    bitshift = 0
    mask = 0xFFFFFFFFFFFFFFFF


class GameSeriesHex(Hex):
    length = 3
    bitshift = GAME_SERIES_BITSHIFT
    mask = GAME_SERIES_MASK


class CharacterHex(Hex):
    length = 4
    bitshift = CHARACTER_BITSHIFT
    mask = CHARACTER_MASK


class VariantHex(Hex):
    length = 6
    bitshift = VARIANT_BITSHIFT
    mask = VARIANT_MASK


class AmiiboTypeHex(Hex):
    length = 2
    bitshift = AMIIBO_TYPE_BITSHIFT
    mask = AMIIBO_TYPE_MASK


class AmiiboModelHex(Hex):
    length = 4
    bitshift = AMIIBO_MODEL_BITSHIFT
    mask = AMIIBO_MODEL_MASK


class AmiiboSeriesHex(Hex):
    length = 2
    bitshift = AMIIBO_SERIES_BITSHIFT
    mask = AMIIBO_SERIES_MASK


class UnknownMask(Hex):
    length = 2
    bitshift = UNKNOWN_BITSHIFT
    mask = UNKNOWN_MASK


class Amiibo:
    def __init__(self, manager, head, tail, name, release, games3DS, gamesWiiU, gamesSwitch):
        self.manager = manager
        self.head = Hex(head)
        self.tail = Hex(tail)
        self.name = name
        self.release = release
        self.games3DS = games3DS
        self.gamesWiiU = gamesWiiU
        self.gamesSwitch = gamesSwitch

    @cached_property
    def id(self):
        return AmiiboHex((self.head << AMIIBO_HEAD_BITSHIFT) + (self.tail << AMIIBO_TAIL_BITSHIFT))

    @cached_property
    def game_series_id(self):
        return GameSeriesHex(self.head)

    @property
    def game_series(self):
        return self.manager.game_series.get(self.game_series_id)

    @cached_property
    def character_id(self):
        return CharacterHex(self.head)

    @property
    def character(self):
        return self.manager.characters.get(self.character_id)

    @cached_property
    def variant_id(self):
        return VariantHex(self.head)

    @cached_property
    def amiibo_type_id(self):
        return AmiiboTypeHex(self.head)

    @property
    def amiibo_type(self):
        return self.manager.types.get(self.amiibo_type_id)

    @cached_property
    def amiibo_model_id(self):
        return AmiiboModelHex(self.tail)

    @cached_property
    def amiibo_series_id(self):
        return AmiiboSeriesHex(self.tail)

    @property
    def amiibo_series(self):
        return self.manager.amiibo_series.get(self.amiibo_series_id)

    @cached_property
    def unknown_id(self):
        return UnknownMask(self.tail)


class AmiiboReleaseDates:
    def __init__(self, na=None, jp=None, eu=None, au=None):
        self.na = na
        self.jp = jp
        self.eu = eu
        self.au = au


class GameSeries:
    def __init__(self, manager, id_, name):
        self.manager = manager
        self.id = GameSeriesHex(id_)
        self.name = name

    @property
    def amiibos(self):
        return (
            amiibo
            for amiibo in self.manager.amiibos
            if amiibo.game_series_id == self.id
        )


class Character:
    def __init__(self, manager, id_, name):
        self.manager = manager
        self.id = CharacterHex(id_)
        self.name = name

    @property
    def amiibos(self):
        return (
            amiibo
            for amiibo in self.manager.amiibos
            if amiibo.character_id == self.id
        )


class AmiiboType:
    def __init__(self, manager, id_, name):
        self.manager = manager
        self.id = AmiiboTypeHex(id_)
        self.name = name

    @property
    def amiibos(self):
        return (
            amiibo
            for amiibo in self.manager.amiibos
            if amiibo.amiibo_type_id == self.id
        )


class AmiiboSeries:
    def __init__(self, manager, id_, name):
        self.manager = manager
        self.id = AmiiboSeriesHex(id_)
        self.name = name

    @property
    def amiibos(self):
        return (
            amiibo
            for amiibo in self.manager.amiibos
            if amiibo.amiibo_series_id == self.id
        )
