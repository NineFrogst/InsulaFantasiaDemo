import csv

# 本程序库主管静态的文件与动态的系统之间的互动。


# LibSys
# 游戏中，最核心的两项数据，便是角色数据与卡牌数据。
# 1. 角色
# 游戏中出现的任何角色，都有自己的角色（Character/c）数据。角色数据的存储结构如下：
# - id/cID：角色的唯一识别码，结构为“特征字母 + 数字代码”，如朵芬的id为“c001”。
#   - 特征字母：“c”代表“船员（Crews）”；“h”代表“敌方（Hostiles）”；“o”代表“其他（Others）”，包括召唤物、中立单位等。
#   - 数字代码：暂时以三位十进制数字表示。
# - name/cName：角色的英文名（为排版方便）
# - group/cGroup：角色的分组，包括船员、敌方、其他（同特征字母）。
# - info/cInfo：信息栏，一个包含*描述性*或*判定用*内容的字典，主要内容有：
#   - zh-name：中文名；
#   - abbr：英文名缩写（组队界面用）
#   - rarity：稀有度（1，2，3）；
#   - class：职业；
#   - dubbing：配音
#   - affiliate：所属阵营；
#   - race：种族；
#   - gender：性别；
#   - age：年龄；
#   - story：角色描述；
#   - dialogue：角色语音；
#   - 有需要可以自行额外添加。
# - ppty/cPpty：属性栏，一个包含*结算用*内容与函数的字典，主要内容有：
#   - health：基础血量；
#   - power：战力，竞技模式用
#   - dodge：闪避率；
#   - crit：暴击率；
#   - debuff-resist：负面效果抵抗率；
#   - death：死亡，如果为'common'则正常退场，否则按照ID执行卡牌技能
#   - death-resist：死亡抵抗率；
#   - basicATK：基础攻击卡/平A（的卡牌ID，下同）；
#   - basicSUP：基础支援卡；
#   - passive：被动技能；
#   - finish：终结技；
#   - 可补充。
# 以上内容均存储于/data/charDB.csv中。
# 2. 卡牌
# 游戏中，任何行为都以卡牌（Card/k）的形式实现。卡牌数据的存储结构与角色数据类似：
# - id/kID：
#   - “a”：攻击卡ATK/attack；“s”：支援卡SUP/support；“m”：召唤卡SMN/summon。除了攻击与召唤以外的卡均归属于支援卡（赛博结缔组织）。
#   - *四位*十进制数字。
# - name/kName
# - group/kGroup
# - info/kInfo：
#   - zh-name；
#   - rarity（金G，银S，铜B）；
#   - class（主动active，被动passive）
#   - user：使用者（人/群体）；
#   - usee：承受者（人/群体）；
#   - 可补充。
# - ppty/kPpty：
#   - cost：0~9，x（全部费用），-1（不可打出）；
#   - effect：函数；
#   - 可补充。
# 以上内容均存储于/data/cardDB.csv中。
# 注1：直接编辑csv时，保存双引号符号需要使用双双引号（""），程序调用将自动转义为单个的双引号：
# 如“Hi, friend”转义为“Hi”和“friend”两栏，“"Hi, friend"”为“Hi, friend”一栏，“""Hi, friend""”为“"Hi”和“friend"”两栏。

# 角色
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
            
        newInfo = eval(self.cInfo)
        if len(self.cName) <= 10:
            newInfo['abbr'] = self.cName
        elif self.cName.find(' ') != -1:
            nameList = self.cName.split()
            if len(nameList[-1]) > 10:
                newInfo['abbr'] = nameList[-1][:8] + '.'
            elif (len(nameList[-1]) + 2*len(nameList) - 2) <= 10:
                for i in range(len(nameList)-1):
                    nameList[i] = nameList[i][0]
                newInfo['abbr'] = '.'.join(nameList)
            else:
                newInfo['abbr'] = nameList[-1]
        else:
            newInfo['abbr'] = self.cName[:8] + '.'
        self.cInfo = str(newInfo)

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
    @classmethod
    def countClear(cls):
        global __countCharacter, __countCrews, __countHostiles, __countOthers
        __countCharacter = 0
        __countCrews = 0
        __countHostiles = 0
        __countOthers = 0
        
# 卡牌
class Card:
    __countCard = 0
    __countATK = 0
    __countSMN = 0
    __countSUP = 0

    def __init__(self,kID,kName,kInfo,kPpty):
        self.kID = str(kID)
        self.kName = str(kName)
        self.kInfo = str(kInfo)
        self.kPpty = str(kPpty)
        Card.__countCard += 1
        if   kID[0] == 'a' :
            self.kGroup = 'ATK'
            Card.__countATK += 1
        elif kID[0] == 'm' :
            self.kGroup = 'SMN'
            Card.__countSMN += 1
        else :
            self.kGroup = 'SUP'
            Card.__countSUP += 1

    def __str__(self):
        return '%s'%({
            'id' : self.kID,
            'name' : self.kName,
            'group' : self.kGroup,
            'info' : self.kInfo,
            'ppty' : self.kPpty
        })
    def __repr__(self):
        return '%s'%({
            'id' : self.kID,
            'name' : self.kName,
            'group' : self.kGroup,
            'info' : self.kInfo,
            'ppty' : self.kPpty
        })
    @classmethod
    def countClear(cls):
        global __countCard, __countATK, __countSMN, __countSUP
        __countCard = 0
        __countATK = 0
        __countSMN = 0
        __countSUP = 0

# 数据库操作
def getIFDB(caseof,mode='get',lookID=None):
    fileDict = {}
    if caseof == 'char': # 整合后的分支判断
        file = './data/charDB.csv'
        classof = Character
        header = ['id','name','稀有度','组别','职业']
        groupList = ['c','h','o']
    elif caseof == 'card':
        file = './data/cardDB.csv'
        classof = Card
        header = ['id','name','稀有度','组别','使用者']
        groupList = ['a','m','s']
    else:
        return print('caseof error')
    
    def grabID(elemDict):
        return elemDict['id']
    def DBUpdate():
        fo = open(file,'r+',encoding='UTF8')
        fileData = list(csv.DictReader(fo))
        fo.close()
        fileData.sort(key=grabID)
        classof.countClear()
        for row in fileData:
            fileObj = classof(row['id'],row['name'],row['info'],row['ppty'])
            fileDict[row['id']] = str(fileObj)

    def modeGet(lookID): # 获取项目
        print('{:<5} {:<15} {:　<3} {:<6} {:<}'.format(header[0],header[1],header[2],header[3],header[4]))
        for k, v in fileDict.items():
            ckID = eval(v)['id']
            ckName = eval(v)['name']
            ckGroup = eval(v)['group']
            try:
                if caseof == 'char':
                    ckRarity = '☆'*eval(eval(eval(v)['info'])['rarity'])
                    ckSp = eval(eval(v)['info'])['class']
                elif caseof == 'card':
                    ckRarity = ['Bronze','Silver','Gold'][eval(eval(eval(v)['info'])['rarity']) - 1]
                    ckSp = eval(eval(v)['info'])['userID']
            except:
                ckRarity = 0
                ckSp = 'null'
            if lookID == groupList[0]:
                if k[0] == groupList[0]:print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(ckID,ckName,ckRarity,ckGroup,ckSp))
            elif lookID == groupList[1]:
                if k[0] == groupList[1]:print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(ckID,ckName,ckRarity,ckGroup,ckSp))
            elif lookID == groupList[2]:
                if k[0] != groupList[1] and k[0] != groupList[0]:print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(ckID,ckName,ckRarity,ckGroup,ckSp))
            else: # 全体
                print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(ckID,ckName,ckRarity,ckGroup,ckSp))
    def modeFind(lookID): # 查找项目
        if lookID not in list(fileDict.keys()):
            print('未找到角色。')
            return {}
        return eval(fileDict[lookID])
    def modeNew(lookID): # 增加角色
        if lookID[0] in list(fileDict.keys()):
            print('ID已占用。')
            return 
        newDict = eval(str(classof(lookID[0],lookID[1],lookID[2],lookID[3])))
        
        fo = open(file,'a+',encoding='UTF8')
        fo.write('\n')
        newItem = csv.DictWriter(fo,['id','name','info','ppty'])
        newRow = newDict
        newRow.pop('group')
        newItem.writerow(newRow)
        print('添加 {} 成功。'.format(lookID[1]))
        fo.close()
        DBUpdate()
        print('Updating......')
        return newDict
    def modeDel(lookID): # 删除项目
        if lookID not in list(fileDict.keys()):
            print('ID不存在。')
            return 
            
        delDict = eval(fileDict.pop(lookID))
        fo = open(file,'w+',encoding='UTF8')
        newFile = csv.DictWriter(fo,['id','name','info','ppty'])
        newRows = []
        for v in fileDict.values():
            i = eval(v)
            i.pop('group')
            newRows.append(i)
        newFile.writeheader()
        newFile.writerows(newRows)
        print('删除 {} 成功。'.format(delDict['name']))
        fo.close()
        DBUpdate()
        print('Updating......')
        return delDict

    DBUpdate()
    if mode == 'get': # 获取项目
        modeGet(lookID)
        return fileDict
    elif mode == 'find': # 查找项目
        return modeFind(lookID)
    elif mode == 'new': # 增加项目
        return modeNew(lookID)
    elif mode == 'del': # 删除项目
        return modeDel(lookID)
    elif mode == 'edit': # 修改项目
        modeDel(lookID[0])
        return modeNew(lookID)
    else:
        print('getIFDB()的mode设置错误，程序中止')

# 向下兼容
def getCharacterDB(mode='get',lookID=None):
    return getIFDB('char',mode,lookID)
def getCardDB(mode='get',lookID=None):
    return getIFDB('card',mode,lookID)



# SquadSys
# squad.csv 文件结构如下：
# preset：预设，默认t00（team）为己方当前队伍、r00（rival）为敌方当前队伍。
# front：前排，列表
# back：后排，列表
# cardset：卡组，列表

# 队伍信息

def getSquad(caseof,mode='now',lookPreset=None):
    squadDict = {}
    if caseof == 'ally':
        defaultSet = 't00'
    elif caseof == 'enemy':
        defaultSet = 'r00'
    else:
        return print('caseof error.')
    
    def grabPreset(elemDict):
        return elemDict['preset']
    def squadUpdate():
        fo = open('./data/squad.csv','r+',encoding='UTF8')
        squadData = list(csv.DictReader(fo))
        fo.close()
        squadData.sort(key=grabPreset)
        for row in squadData:
            squadDict[row['preset']] = str(row)
    
    def modeNow():
        return squadDict[defaultSet]
    def modeFind(lookPreset):
        try:
            return squadDict[lookPreset]
        except:
            print('未找到预设。')
            return
    def modeNew(lookPreset):
        if lookPreset['preset'] in list(squadDict.keys()):
            print('预设已存在。')
            return
        fo = open('./data/squad.csv','a+',encoding='UTF8')
        newPreset = csv.DictWriter(fo,['preset','front','back','cardset'])
        newPreset.writerow(lookPreset)
        fo.close()
        print('创建 {} 成功。'.format(lookPreset['preset']))
        squadUpdate()
        print('Updating......')
        return lookPreset
    def modeDel(lookPreset):
        if lookPreset not in list(squadDict.keys()):
            print('预设不存在。')
            return
        delPreset = squadDict.pop(lookPreset)
        fo = open('./data/squad.csv','w+',encoding='UTF8')
        newFile = csv.DictWriter(fo,['preset','front','back','cardset'])
        newFile.writeheader()
        newFile.writerows([eval(v) for v in squadDict.values()])
        fo.close()
        print(f'删除 {lookPreset} 成功。')
        squadUpdate()
        print('Updating......')
        return delPreset
    
    squadUpdate()
    if mode == 'now':
        return modeNow()
    elif mode == 'get':
        return squadDict
    elif mode == 'find':
        return modeFind(lookPreset)
    elif mode == 'new':
        return modeNew(lookPreset)
    elif mode == 'del':
        return modeDel(lookPreset)
    elif mode == 'edit':
        modeDel(lookPreset['preset'])
        return modeNew(lookPreset)
    else:
        print('getSquad()的mode设置错误，程序中止')