import csv

class Character:
    __countCharacter = 0
    __countCrews = 0
    __countHostiles = 0
    __countOthers = 0

    def __init__(self,cID,cName,cInfo,cPpty):
        self.cID = str(cID)
        self.cName = str(cName)
        self.cInfo = str(cInfo)
        self.cPpty = str(cPpty)
        Character.__countCharacter += 1
        if   cID[0] == 'c' :
            self.cGroup = 'Crews'
            Character.__countCrews += 1
        elif cID[0] == 'h' :
            self.cGroup = 'Hostiles'
            Character.__countHostiles += 1
        else :
            self.cGroup = 'Others'
            Character.__countOthers += 1

    def __str__(self):
        return '%s'%({
            'id' : self.cID,
            'name' : self.cName,
            'group' : self.cGroup,
            'info' : self.cInfo,
            'ppty' : self.cPpty
        })
    def __repr__(self):
        return '%s'%({
            'id' : self.cID,
            'name' : self.cName,
            'group' : self.cGroup,
            'info' : self.cInfo,
            'ppty' : self.cPpty
        })
    def basicATK(self,*args,**kwargs):
        try:
            exec(eval(self.cPpty)['basicATK'])
        except:
            pass
    
def getCharacterDB(mode='get',lookID=None):
    charDict = {}
    def charDBUpdate():
        fo = open('./data/charDB.csv','r+',encoding='UTF8')
        charData = list(csv.DictReader(fo))
        fo.close()
        for row in charData:
            charObj = Character(row['id'],row['name'],row['info'],row['ppty'])
            charDict[row['id']] = str(charObj)

    def modeGet(lookID): # 获取角色
        print('{:<5} {:<15} {:　<3} {:<8} {:<}'.format('id','name','稀有度','职业','声优'))
        for k, v in charDict.items():
            cID = eval(v)['id']
            cName = eval(v)['name']
            try:
                cRarity = eval(eval(eval(v)['info'])['rarity'])
                cClass = eval(eval(v)['info'])['class']
                cDubbing = eval(eval(v)['info'])['dubbing']
            except:
                cRarity = 0
                cClass = 'null'
                cDubbing = 'null'
            if lookID == 'crews': # 船员
                if k[0] == 'c':print('{:<5} {:<15} {:　<3} {:<10} {:<}'.format(cID,cName,cRarity*'☆ ',cClass,cDubbing))
            elif lookID == 'hostiles': # 敌方
                if k[0] == 'h':print('{:<5} {:<15} {:　<3} {:<10} {:<}'.format(cID,cName,cRarity*'☆ ',cClass,cDubbing))
            elif lookID == 'others': # 其他
                if k[0] != 'c' and k[0] != 'h':print('{:<5} {:<15} {:　<3} {:<10} {:<}'.format(cID,cName,cRarity*'☆ ',cClass,cDubbing))
            else: # 全体
                print('{:<5} {:<15} {:　<3} {:<10} {:<}'.format(cID,cName,cRarity*'☆ ',cClass,cDubbing))
    def modeFind(lookID): # 查找角色
        try:
            v = charDict[lookID]
            cID = eval(v)['id']
            cName = eval(v)['name']
            try:
                cRarity = eval(eval(eval(v)['info'])['rarity'])
                cClass = eval(eval(v)['info'])['class']
                cDubbing = eval(eval(v)['info'])['dubbing']
            except:
                cRarity = 0
                cClass = 'null'
                cDubbing = 'null'
            print('{:<5} {:<15} {:　<3} {:<8} {:<}'.format('id','name','稀有度','职业','声优'))
            print('{:<5} {:<15} {: <6} {:<10} {:<}'.format(cID,cName,cRarity*'☆ ',cClass,cDubbing))
        except:
            print('未找到角色。')
    def modeNew(lookID):
        if lookID[0] in list(charDict.keys()):
            print('ID已占用。')
            return 
        	
        newDict = {}
        newDict['id'] = lookID[0]
        newDict['name'] = lookID[1]
        newDict['info'] = {}
        newDict['ppty'] = {}
        newDict['info']['rarity'] = lookID[2]
        newDict['info']['class'] = lookID[3]
        newDict['info']['dubbing'] = lookID[4]
        
        newDict = eval(str(Character(newDict['id'],newDict['name'],newDict['info'],newDict['ppty'])))
        
        fo = open('./data/charDB.csv','a+',encoding='UTF8')
        fo.write('\n{},"{}","{}","{}"'.format(newDict['id'],newDict['name'],newDict['info'],newDict['ppty']))
        print('添加 {} 成功。'.format(lookID[1]))
        fo.close()
        
        return newDict
    def modeDel(lookID):
        if lookID not in list(charDict.keys()):
            print('ID不存在。')
            return 
            
        delDict = eval(charDict.pop(lookID))
        print('删除 {} 成功。'.format(delDict['name']))
        fo = open('./data/charDB.csv','w+',encoding='UTF8')
        fo.write('id,name,info,ppty')
        for k, v in charDict.items():
            newDict = eval(v)
            fo.write('\n{},"{}","{}","{}"'.format(newDict['id'],newDict['name'],newDict['info'],newDict['ppty']))
        fo.close()
        
        
        return delDict

    charDBUpdate()
    if mode == 'get':
        modeGet(lookID)
        return charDict
    elif mode == 'find':
        modeFind(lookID)
        try:
            return charDict[lookID]
        except:
            return 
    elif mode == 'new':
        newDict = modeNew(lookID)
        print('Updating......')
        charDBUpdate()
        return newDict
    elif mode == 'del':
        delDict = modeDel(lookID)
        print('Updating......')
        charDBUpdate()
        return delDict
    elif mode == 'edit':
        modeDel(lookID[0])
        newDict = modeNew(lookID)
        print('Updating......')
        charDBUpdate()
        return newDict
    else:
        print('getCharacterDB()的mode设置错误，程序中止')