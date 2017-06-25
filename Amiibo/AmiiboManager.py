#!/usr/bin/env python
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""

from Amiibo import Amiibo, AmiiboDate
import sqlite3

class amiiboManager():

    def __init__(self):
        # Initialize sqlite
        self.conn = sqlite3.connect('database/database.db')
        self.c = self.conn.cursor()

        self.amiiboList = self.generateAmiiboData()
        self.charList = self.generateDictData("character")
        self.amiiboSeriesList = self.generateDictData("amiiboSeries")
        self.typeList = self.generateDictData("type")
        self.gameSeries = self.generateDictData("gameSeries")
        self.releaseDates = self.generateReleaseDate()

        # Close all sqlite connection.
        self.conn.close()

    ############################### Initialize generator ###############################

    # generate amiiboData from database.
    def generateAmiiboData(self):
        amiibo = list();

        # For each value in data we make it into an amiibo object.
        for row in self.c.execute('SELECT * FROM amiibo ORDER BY name'):
                newAmiibo = Amiibo.amiibo(row[0], row[1], row[2])
                amiibo.append(newAmiibo)
        return amiibo

    # generate dict of item from database base on table name. Usually use for table with key and name only.
    def generateDictData(self, tableName):
        result = dict()

        for row in self.c.execute('SELECT * FROM '+ tableName +' ORDER BY name'):
            result.update({hex(int(row[0],16)):row[1]})

        return result

    # generate release date information
    def generateReleaseDate(self):
        result = dict()

        for row in self.c.execute('SELECT * FROM releaseDate ORDER BY id'):
            na = row[1]
            jp = row[2]
            eu = row[3]
            au = row[4]

            if na is None:
                na = "None"
            if jp is None:
                jp = "None"
            if eu is None:
                eu = "None"
            if au is None:
                au = "None"

            newReleaseDate = AmiiboDate.amiiboDate(row[0], na, jp, eu, au)
            result.update({row[0]:newReleaseDate})

        return result

    ############################### Getter ###############################

    # Get the game series of the amiibo.
    def getAmiiboGameSeries(self, amiibo):
        value = amiibo.getHead()[0:3]
        value = hex(int(value, 16))
        return self.gameSeries.get(value), value

    # Get the type of the amiibo.
    def getAmiiboType(self, amiibo):
        head = amiibo.getHead()
        char = head[-2:len(head)]
        return self.typeList.get(hex(int(char, 16))), hex(int(char, 16))

    # Get the character of the amiibo.
    def getAmiiboCharacter(self, amiibo):
        head = amiibo.getHead()
        value = head[0:4]
        return self.charList.get(hex(int(value, 16))), hex(int(value, 16))

    # Get the series of the amiibo.
    def getAmiiboSeries(self, amiibo):
        value = amiibo.getTail()[-4:-2]
        result = self.amiiboSeriesList.get(hex(int(value, 16)))
        return result, hex(int(value, 16))

    # Get the release date of the amiibo.
    def getReleaseDate(self, id):
        releaseDate = self.releaseDates.get(id)
        na = releaseDate.getNorthAmerica()
        jp = releaseDate.getJapan()
        eu = releaseDate.getEurope()
        au = releaseDate.getAustralia()
        return na, jp, eu, au

if __name__ == "__main__":
    m = amiiboManager()
    # Bokoblin
    amiibo = m.amiiboList[1]
    # Get the type.
    print(m.getAmiiboType(amiibo))
    # Get the character
    print(m.getAmiiboCharacter(amiibo))
    # Get the series
    print(m.getAmiiboSeries(amiibo))
    # get the game series.
    print(m.getAmiiboGameSeries(amiibo))
