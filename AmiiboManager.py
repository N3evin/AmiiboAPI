import glob, Amiibo
class amiiboManager():

    def __init__(self):
        self.amiiboList = self.generateAmiiboData()
        self.charList = self.generateDictData("database/character.txt")
        self.amiiboSeriesList = self.generateDictData("database/info/amiibo_series.txt")
        self.typeList = self.generateDictData("database/info/type.txt")
        self.gameSeries = self.generateGameSeries()

    # generate amiiboData from database folder.
    def generateAmiiboData(self):

        files = list();

        # Read all the files in the database.
        for file in glob.glob("database/name/*.txt"):
            files.append(file)

        amiibo = list();

        # Go through each files in the directory.
        for name in files:
            # Open each file and read the lines.
            with open(name, "r", encoding="utf8") as file:
                data =  file.read().splitlines()

            # For each value in data we make it into an amiibo object.
            for value in data:
                if(len(value) > 0 and value[0] != "#"):
                    value = value.split(', ')
                    newAmiibo = Amiibo.amiibo(value[0], value[1].rstrip(' '), value[2].rstrip(' '))
                    amiibo.append(newAmiibo)
        return amiibo

    # generatea dict of item from database folder.
    def generateDictData(self, fileName):
        result = dict();
        with open(fileName, "r", encoding="utf8") as f:
            data = f.read().splitlines();

        for item in data:
            if (len(item) > 0 and item[0] != "#"):
                item = item.split(',')
                result.update({hex(int(item[1].rstrip(' '),16)):item[0]})

        return result

    # generate a dict of game series.
    def generateGameSeries(self):
        result = dict();
        with open("database/info/game_series.txt", "r", encoding="utf8") as f:
            data = f.read().splitlines();

        for item in data:
            if (len(item) > 0 and item[0] != "#"):
                item = item.split(',')
                if (len(item) == 3):
                    value1 = int(item[1].rstrip(' '), 16)
                    value2 = int(item[2].rstrip(' '), 16)
                    while (value1 <= value2):
                        result.update({hex(value1): item[0]})
                        value1 += 1
                else:
                    result.update({hex(int(item[1],16)): item[0]})

        return result

    # Get the game series of the amiibo.
    def getAmiiboGameSeries(self, amiibo):
        value = amiibo.getHead()[0:3]
        value = hex(int(value, 16))
        return self.gameSeries.get(value)

    # Get the type of the amiibo.
    def getAmiiboType(self, amiibo):
        head = amiibo.getHead()
        char = head[-2:len(head)]
        return self.typeList.get(hex(int(char, 16)))

    # Get the character of the amiibo.
    def getAmiiboCharacter(self, amiibo):
        head = amiibo.getHead()
        value = head[0:4]
        return self.charList.get(hex(int(value, 16)))

    # Get the character of the amiibo.
    def getAmiiboSeries(self, amiibo):
        value = amiibo.getTail()[-4:-2]
        result = self.amiiboSeriesList.get(hex(int(value, 16)))
        return result

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
