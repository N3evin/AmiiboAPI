#!/usr/bin/env python
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""

class amiiboDate(object):

    # Constructor
    def __init__(self, id, na, jp, eu, au):
        self.id = id
        self.na = na
        self.jp = jp
        self.eu = eu
        self.au = au

    # Get the ID for the release date
    def getId(self):
        return self.id

    # Get North America release date
    def getNorthAmerica(self):
        return self.na

    # Get Japan release date
    def getJapan(self):
        return self.jp

    # Get Europe release date
    def getEurope(self):
        return self.eu

    # Get Australia release date
    def getAustralia(self):
        return self.au