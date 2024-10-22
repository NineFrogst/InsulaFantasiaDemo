import csv

class Character:
    __countCharacter = 0
    __countCrews = 0
    __countHostiles = 0
    __countOthers = 0

    def __init__(self,cID,cName,cInfo,cPpty):
        self.cID = str(cID)
        self.cName = str(cName)
        self.cInfo = eval(str(cInfo))
        self.cPpty = eval(str(cPpty))
        Character.__countCharacter += 1
        if   cID[0] == 'c' :
            self.cClass = 'Crews'
            Character.__countCrews += 1
        elif cID[0] == 'h' :
            self.cClass = 'Hostiles'
            Character.__countHostiles += 1
        else :
            self.cClass = 'Others'
            Character.__countOthers += 1

    def __str__(self):
        return '%s'%({
            'id' : self.cID,
            'name' : self.cName,
            'class' : self.cClass,
            'info' : self.cInfo,
            'ppty' : self.cPpty
        })
    def __repr__(self):
        return '%s'%({
            'id' : self.cID,
            'name' : self.cName,
            'class' : self.cClass,
            'info' : self.cInfo,
            'ppty' : self.cPpty
        })
    
def getCharacterDB():
    fo = open('./data/charDB.csv','r+',encoding='UTF8')
    charData = csv.reader(fo)