import Amiibo, sqlite3
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

        # Close all sqlite connection.
        self.conn.close()

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

    # Get the character of the amiibo.
    def getAmiiboSeries(self, amiibo):
        value = amiibo.getTail()[-4:-2]
        result = self.amiiboSeriesList.get(hex(int(value, 16)))
        return result, hex(int(value, 16))

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
