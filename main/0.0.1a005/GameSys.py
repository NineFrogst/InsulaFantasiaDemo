from FeatureFuncs import *
from DataIO import *
import random

# 游戏界面
def PageGame(breakCode=None):
    if breakCode != 1:
        print("-----------\n幻 岛 缘 游\n-----------\n游戏启动中......")
        loading()
        Game.resetGame()
        gameRoutine()
    return 1

def cardPlay(cardDict,userObj,useeObj):
    kPpty = eval(cardDict['ppty'])
    if Game.costNow >= int(kPpty['cost']):
        print('{} 对 {} 使用了 {} ！'.format(userObj.cName,useeObj.cName,cardDict['name']))
        Game.costNow -= int(kPpty['cost'])
        return kPpty['effect']
    else:
        return '1' # 暂时想不出更好的跳过方式
    
class Entity:
    def __init__(self,cID):
        charDict = getCharacterDB('find',str(cID))
        self.cID = str(cID)
        self.cName = str(charDict['name'])
        self.cAbbr = str(eval(charDict['info'])['abbr'])
        self.cPpty = eval(charDict['ppty'])
        self.HP = eval(self.cPpty['health'])
        # if self.cPpty['health'][0] in [str(i) for i in range(10)]: self.HP = eval(self.cPpty['health'])
        # else: return 'false health'
        # 早点加上上面这些防注入判断

    def takeHealing(self,points):
        print(f'{self.cName} 恢复了 {points} 点生命！')
        if self.HP + points >= eval(self.cPpty['health']):
            self.HP = eval(self.cPpty['health'])
        else:
            self.HP += points
        print(f'{self.cName} 当前HP：{self.HP}')
    def takeDamage(self,userObj,points):
        print(f'{self.cName} 失去了 {points} 点生命！')
        if points >= self.HP:
            self.HP = 0
            self.takeDeath(userObj,self)
        else:
            self.HP -= points
            print(f'{self.cName} 当前HP：{self.HP}')
    def takeDeath(self,userObj,useeObj):
        if self.cPpty['death'] == 'common':
            print(f'{self.cName} 被 {userObj.cName} 杀死了！')
            return Game.commonDeath(self)
        try:
            cardDict = eval(getCardDB('find',self.cPpty['death']))
            exec(cardPlay(cardDict,userObj,useeObj))
        except:
            return print(f'{self.cName} death error.')
    def basicATK(self,userObj,useeObj):
        try:
            cardDict = eval(getCardDB('find',self.cPpty['basicATK']))
            exec(cardPlay(cardDict,userObj,useeObj))
        except:
            return print(f'{self.cName} basicATK error.')
    def basicSUP(self,userObj,useeObj):
        try:
            cardDict = eval(getCardDB('find',self.cPpty['basicSUP']))
            exec(cardPlay(cardDict,userObj,useeObj))
        except:
            return print(f'{self.cName} basicSUP error.')
    def passive(self,userObj,useeObj):
        try:
            cardDict = eval(getCardDB('find',self.cPpty['passive']))
            exec(cardPlay(cardDict,userObj,useeObj))
        except:
            return print(f'{self.cName} passive error.')

class Game:
    COSTLIMIT = 6
    costNow = 6 # 以后可能出现开局爆cost或者提高cost上限的情况，分成两个参数
    allySquad = eval(getSquad('ally','now'))
    enemySquad = eval(getSquad('enemy','now')) # 之后这两个squad只会用来储存卡牌数据deck、hand、discard、consume

    def __init__(self):
        allySquad = eval(getSquad('ally','now'))
        enemySquad = eval(getSquad('enemy','now'))
        allyFront = []
        allyBack = []
        enemyFront = []
        enemyBack = []
        squadList = [enemySquad['back'],enemySquad['front'],allySquad['front'],allySquad['back']]
        entityList = [enemyBack,enemyFront,allyFront,allyBack]
        for i in range(4):
            charList = eval(squadList[i])
            objList = entityList[i]
            for j in range(len(charList)):
                objList.append(Entity(charList[j]))
        Game.entityList = entityList
        Game.allySquad['deck'] = []
        Game.allySquad['hand'] = []
        Game.allySquad['discard'] = []
        Game.allySquad['consume'] = []
        Game.enemySquad['deck'] = []
        Game.enemySquad['hand'] = []
        Game.enemySquad['discard'] = []
        Game.enemySquad['consume'] = []
        for kID in eval(allySquad['cardset']):
            Game.allySquad['deck'].append(getCardDB('find',kID))
        for kID in eval(enemySquad['cardset']):
            Game.enemySquad['deck'].append(getCardDB('find',kID))
        random.seed()
        random.shuffle(Game.allySquad['deck'])
        random.shuffle(Game.enemySquad['deck']) # initialize: shuffle deck
    
    @classmethod
    def resetGame(cls):
        Game.COSTLIMIT = 6
        Game.costNow = 6
        Game.allySquad = eval(getSquad('ally','now'))
        Game.enemySquad = eval(getSquad('enemy','now'))

    @staticmethod
    def commonDeath(charObj):
        for row in Game.entityList:
            if charObj in row:
                row.remove(charObj)
                break
            else:
                return print(f'{charObj.cName} not found.')

def gameBattlefield(entityList):
    loading()
    print('__|{:_<10}|{:_<10}|{:_<10}|{:_<10}|{:_<10}|'.format('1','2','3','4','5'))
    for i in range(4):
        print('{}'.format(['eB','eF','aF','aB'][i]), end='|')
        for entityObj in entityList[i]:
            print('{:<10}'.format(entityObj.cAbbr), end=' ')
        print()
        if i == 1 or i == 3:
            print('--|{:-<10}|{:-<10}|{:-<10}|{:-<10}|{:-<10}|'.format('','','','',''))

def gameAction(squad):
    gameBattlefield(Game.entityList) # 绘制战场
    print(f'当前cost：{Game.costNow}/{Game.COSTLIMIT}') # 展示费用
    print('手牌：')
    for i in range(len(squad['hand'])):
        print('{:>2}. {}'.format(i+1,squad['hand'][i]['name'])) # 展示手牌
    gameAct = str(input('1. 出牌 2. 牌堆 3. 弃牌堆 4. 消耗牌堆 5. 结束回合\n0. 退出\n请选择：'))
    if gameAct == '0':
        if str(input('确认退出？（y/n）')) == 'y':
            return True
    elif gameAct == '1':
        try:
            cardSelect = int(input('请选择卡牌（序号）：'))
        except:
            print('卡牌选择错误。')
            return gameAction(squad)
        userOrd = str(input('请选择施放角色（先行后列，如eB1）：'))
        userY = ['eB','eF','aF','aB'].index(userOrd[0:2])
        userX = int(userOrd[2]) - 1
        userObj = Game.entityList[userY][userX]
        if userObj.cID not in eval(squad['front']) and userObj.cID not in eval(squad['back']):
            print('施放角色选择错误。')
            return gameAction(squad)
        useeOrd = str(input('请选择施放对象（先行后列，如eB1）：'))
        useeY = ['eB','eF','aF','aB'].index(useeOrd[0:2])
        useeX = int(useeOrd[2]) - 1
        useeObj = Game.entityList[useeY][useeX]
        loading()
        if eval(cardPlay(squad['hand'][cardSelect-1],userObj,useeObj)) == 1:
            print('费用不足！')
        else:
            squad['hand'].remove(squad['hand'][cardSelect-1])
    elif gameAct == '2':
        print('抽牌堆：')
        def grabID(elemDict):
            return elemDict['id']
        deckNow = squad['deck']
        deckNow.sort(key=grabID)
        for i in range(len(deckNow)):
            print('{:>2}. {}'.format(i+1,deckNow[i]['name']))
        input('按任意键返回......')
    elif gameAct == '3':
        print('弃牌堆：')
        for i in range(len(squad['discard'])):
            print('{:>2}. {}'.format(i+1,squad['discard'][i]['name']))
        input('按任意键返回......')
    elif gameAct == '4':
        print('消耗牌堆：')
        for i in range(len(squad['consume'])):
            print('{:>2}. {}'.format(i+1,squad['consume'][i]['name']))
        input('按任意键返回......')
    else:
        if gameIsWin():
            return True
        return False
    
    if gameIsWin():
        return True
    return gameAction(squad)

def gameDrawCard(squad,cardNum):
    deckLength = len(squad['deck'])
    if deckLength >= cardNum:
        for i in range(cardNum):
            squad['hand'].append(squad['deck'].pop())
        return
    else:
        gameDrawCard(squad,deckLength)
        squad['deck'] = squad['discard']
        squad['discard'].clear()
        random.seed()
        random.shuffle(squad['deck'])
        gameDrawCard(squad,cardNum-deckLength)

def gameTurn(squad):
    # Before
    gameDrawCard(squad,cardNum=5) # draw cards to hand
    Game.costNow = Game.COSTLIMIT # refill the cost
    # During
    if gameAction(squad):
        return True
    # After
    Game.costNow = 0 # 以后可以添加默认保留费用的能力
    squad['discard'].extend(squad['hand']) # 以后可以添加未使用则消耗的卡牌
    squad['hand'].clear() # 以后可以添加可保留卡牌
    return False

def gameIsWin():
    if len(Game.entityList[0]) + len(Game.entityList[1]) == 0:
        print('我方胜利！')
    elif len(Game.entityList[2]) + len(Game.entityList[3]) == 0:
        print('敌方胜利！')
    else:
        return False
    return True

def gameRoutine():
    initGame = Game() # initialize
    isEnd = False
    while True:
        print('我方回合：')
        isEnd = gameTurn(Game.allySquad)
        if isEnd == True:
            break
        loading()
        print('敌方回合：')
        isEnd = gameTurn(Game.enemySquad)
        if isEnd == True:
            break
    