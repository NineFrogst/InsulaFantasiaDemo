from FeatureFuncs import *
from DataIO import *
import random

# 游戏界面
def PageGame(breakCode=None):
    '''
    整个游戏的核心——游戏系统。
    游戏界面的主界面。
    暂时会直接跳转到游戏实际界面。
    暂时处于沙盒模式（可操作敌我双方）。

    最后一个开发的主要文件。
    前面的程序设计和信息获取都是为此打基础。

    可传入参数breakCode，直接退出游戏或重新开始游戏。

    TODO: 卡牌使用对象判定，护甲值，状态赋予与查看（血量、护甲、持续性状态），特殊卡牌，敌方AI，抽牌上限。
    TODO: 召唤牌在场上位置不够时无法使用的判断语句。
    '''
    if breakCode != 1:
        print("-----------\n幻 岛 缘 游\n-----------\n游戏启动中......")
        loading()
        # Game.resetGame()
        gameRoutine()
    return 1

def cardPlay(cardDict,userObj,useeObj,game):
    '''
    打出当前卡牌。

    传入卡牌字典cardDict、施动对象userObj、受动对象useeObj三个参数，并检测当前剩余费用是否足够使用卡牌。
    如果费用足够则打出卡牌并输出使用声明，随后扣除费用并执行卡牌使用的函数字符串，返回True。如果不够则返回 False 。

    TODO: 反注入，卡牌函数报错时的处理。
    TODO: 可能可以设置某种处理函数，涵盖游戏中出现的主要情况，然后为卡牌效果设置一种特殊的书写格式，依靠处理函数转义为python语句。
    '''
    kPpty = eval(cardDict['ppty'])
    if game.costNow >= int(kPpty['cost']):
        print('{} 对 {} 使用了 {} ！'.format(userObj.cName,useeObj.cName,cardDict['name']))
        game.costNow -= int(kPpty['cost'])
        exec(kPpty['effect'])
        return True
    else:
        print('费用不足！')
        return False
    
class Entity:
    '''
    角色在从数据库里的数据变成游戏战场上的一员之前，要先经过实体类（Entity）并成为其的实例。

    成为实体的实例（对象）后，程序会赋予其特定的id（并非数据库中的id，更像内存地址），使得施动、受动、退场时，能锁定到该对象，而不会出现同名角色全部退场的bug。
    为便于调用，实体包含角色的绝大部分属性与数据。
    '''
    def __init__(self,cID):
        '''按照cID查找角色数据后，将返回的字典中对应的数据保存到对象的属性里。'''
        charDict = getCharacterDB('find',str(cID))
        self.cID = str(cID)
        self.cName = str(charDict['name'])
        self.cInfo = eval(charDict['info'])
        self.cAbbr = str(self.cInfo['abbr'])
        self.cPpty = eval(charDict['ppty'])
        self.HP = eval(self.cPpty['health'])
        self.side = ''
        self.status = {}
        self.situation = None
        # if self.cPpty['health'][0] in [str(i) for i in range(10)]: self.HP = eval(self.cPpty['health'])
        # else: return 'false health'
        # 早点加上上面这些防注入判断

    def takeHealing(self,points):
        '''公开调用的治疗方法，达到血量上限时不再额外提升血量。因UI问题，为方便，自动输出当前血量。'''
        print(f'{self.cName} 恢复了 {points} 点生命！')
        if self.HP + points >= eval(self.cPpty['health']):
            self.HP = eval(self.cPpty['health'])
        else:
            self.HP += points
        print(f'{self.cName} 当前HP：{self.HP}')
    def takeDamage(self,userObj,points):
        '''公开调用的受伤方法，血量归零时调用死亡方法。结束时自动输出当前血量。'''
        print(f'{self.cName} 失去了 {points} 点生命！')
        if points >= self.HP:
            self.HP = 0
            self.takeDeath(userObj,self)
        else:
            self.HP -= points
            print(f'{self.cName} 当前HP：{self.HP}')
    def takeDeath(self,userObj,useeObj,game):
        '''公开调用的死亡方法，角色死亡属性未特殊设置时调用Game类的commonDeath()方法。（主要是为了不死的Nosferatu留的）'''
        if self.cPpty['death'] == 'common':
            print(f'{self.cName} 被 {userObj.cName} 杀死了！')
            return game.commonDeath(self)
        try:
            cardDict = eval(getCardDB('find',self.cPpty['death']))
            exec(cardPlay(cardDict,userObj,useeObj,game))
        except:
            return print(f'{self.cName} death error.')
    def basicATK(self,userObj,useeObj,game):
        '''普通攻击，调用普通攻击属性里的kID查找卡牌。'''
        try:
            cardDict = eval(getCardDB('find',self.cPpty['basicATK']))
            exec(cardPlay(cardDict,userObj,useeObj,game))
        except:
            return print(f'{self.cName} basicATK error.')
    def basicSUP(self,userObj,useeObj,game):
        '''普通支援技能，调用普通支援属性里的kID查找卡牌。'''
        try:
            cardDict = eval(getCardDB('find',self.cPpty['basicSUP']))
            exec(cardPlay(cardDict,userObj,useeObj,game))
        except:
            return print(f'{self.cName} basicSUP error.')
    def passive(self,userObj,useeObj,game):
        '''被动技能，调用被动技能属性里的kID查找卡牌。（暂时没想好怎么交互）'''
        try:
            cardDict = eval(getCardDB('find',self.cPpty['passive']))
            exec(cardPlay(cardDict,userObj,useeObj,game))
        except:
            return print(f'{self.cName} passive error.')

class Game:
    '''
    存储游戏运行时主要数据的类，最开始命名为EntityList（因为需要反复查找实体列表）

    实例化后，主要属性有实体列表、当前费用（costNow）、费用上限（COSTLIMIT，主要作用是确定游戏每轮回复的费用）、我方与敌方编队、我方与敌方牌组等。
    实体列表按照“敌方后排，敌方前排，我方前排，我方后排”的顺序，保存一个内含四个列表的列表。
    '''
    

    def __init__(self):
        '''初始化时，把预设中的角色以实体对象的格式放入实体列表（Game.entityList），把预设中的牌以字典的格式洗进抽牌堆。'''
        self.COSTLIMIT = 6
        self.costNow = 6 # 以后可能出现开局爆cost或者提高cost上限的情况，分成两个参数
        self.allySquad = eval(getSquad('ally','now'))
        self.enemySquad = eval(getSquad('enemy','now')) # 之后这两个squad只会用来储存卡牌数据deck、hand、discard、consume
        allySquad = self.allySquad
        enemySquad = self.enemySquad
        squadList = [allySquad['front'],allySquad['back'],enemySquad['front'],enemySquad['back']]
        newList = []
        for i in range(4):
            charList = eval(squadList[i]) # 记得做防注入
            objList = []
            side = ['ally','ally','enemy','enemy'][i]
            for cID in charList:
                charObj = Entity(cID)
                charObj.side = side
                objList.append(charObj)
            newList.append(objList)
        self.entityList = {'ally':[newList[0],newList[1]],'enemy':[newList[2],newList[3]]}
        del newList

        self.allySquad.update({'deck':[],'hand':[],'discard':[],'consume':[]})
        self.enemySquad.update({'deck':[],'hand':[],'discard':[],'consume':[]})
        for kID in eval(allySquad['cardset']):
            self.allySquad['deck'].append(getCardDB('find',kID))
        for kID in eval(enemySquad['cardset']):
            self.enemySquad['deck'].append(getCardDB('find',kID))
        random.seed()
        random.shuffle(self.allySquad['deck'])
        random.shuffle(self.enemySquad['deck']) # initialize: shuffle deck
    
    # @classmethod
    # def resetGame(cls):
    #     '''刷新重置Game的几个初始属性。（暂时用不上）'''
    #     Game.COSTLIMIT = 6
    #     Game.costNow = 6
    #     Game.allySquad = eval(getSquad('ally','now'))
    #     Game.enemySquad = eval(getSquad('enemy','now'))

    def commonDeath(self,charObj):
        '''常规死亡方法，即直接把角色的实体对象从实体列表中移除。根本就没死只是退场好吧……'''
        for side in self.entityList.values():
            for row in side:
                if charObj in row:
                    row.remove(charObj)
                    return
        else:
            return print(f'{charObj.cName} not found.')

def gameBattlefield(entityList):
    '''打印战场情况，根据entityList的内容按照顺序输出。'''
    loading()
    allyList = entityList['ally'].copy()
    enemyList = entityList['enemy'].copy()
    enemyList.reverse()
    printList = enemyList + allyList
    print('__|{:_<10}|{:_<10}|{:_<10}|{:_<10}|{:_<10}|'.format('1','2','3','4','5'))
    for i in range(4):
        print('{}'.format(['eB','eF','aF','aB'][i]), end='|')
        for entityObj in printList[i]:
            print('{:<10}'.format(entityObj.cAbbr), end=' ')
        print()
        if i == 1 or i == 3:
            print('--|{:-<10}|{:-<10}|{:-<10}|{:-<10}|{:-<10}|'.format('','','','',''))

def gameAction(squad,game):
    '''
    游戏操作进程。（核心）

    每回合流程：绘制战场→展示当前费用和手牌→提供选项
    出牌：选择手牌→选择施动者（含判断，只能为我方）→选择受动者→出牌→判断是否胜利
    各个牌堆：直接读取牌堆（除了抽牌堆会自动整理卡牌顺序，防止千里眼）。
    结束回合：函数返回 False 并结束。
    '''
    while True:
        gameBattlefield(game.entityList) # 绘制战场
        print(f'当前cost：{game.costNow}/{game.COSTLIMIT}') # 展示费用
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
                continue
            try:
                userOrd = str(input('请选择施放角色（先行后列，如aB1）：'))
                userY = ['aF','aB','eF','eB'].index(userOrd[0:2])
                userX = int(userOrd[2]) - 1
                userObj = game.entityList[['ally','ally','enemy','enemy'][userY]][userY % 2][userX]
                if userObj.cID not in eval(squad['front']) and userObj.cID not in eval(squad['back']):
                    print('施放角色选择错误。')
                    continue
                useeOrd = str(input('请选择施放对象（先行后列，如eB1）：'))
                useeY = ['aF','aB','eF','eB'].index(useeOrd[0:2])
                useeX = int(useeOrd[2]) - 1
                useeObj = game.entityList[['ally','ally','enemy','enemy'][useeY]][useeY % 2][useeX]
            except:
                print('出牌程序错误，可能是未找到角色或选择角色错误。')
                continue
            loading()
            if cardPlay(squad['hand'][cardSelect-1],userObj,useeObj,game):
                squad['hand'].remove(squad['hand'][cardSelect-1])
            if gameIsWin(game):
                return True
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
            return False

def gameDrawCard(squad,cardNum):
    '''
    每回合开始时的抽牌环节。

    传入参数cardNum为抽牌数。
    牌堆足够时则将牌堆前cardNum张牌放入手牌，不足时先将弃牌堆洗牌后放入牌堆，再把前cardNum张牌放入手牌。
    如果仍然不足，则洗牌后抽取所有牌，并输出牌堆不足信息。
    '''
    while True:
        if len(squad['deck']) >= cardNum:
            squad['hand'].extend(squad['deck'][0:cardNum])
            squad['deck'] = squad['deck'][cardNum:]
            break
        elif len(squad['deck']) + len(squad['discard']) < cardNum:
            random.seed()
            random.shuffle(squad['discard'])
            squad['deck'].extend(squad['discard'])
            squad['hand'].extend(squad['deck'])
            print('我的牌堆不足了！')
            squad['deck'].clear()
            squad['discard'].clear()
            break
        else:
            random.seed()
            random.shuffle(squad['discard'])
            squad['deck'].extend(squad['discard'])
            squad['discard'].clear()

def gameTurn(squad,game):
    '''
    游戏回合进程。

    抽牌并回复费用→循环检测操作直到结束回合→清空当前费用，手牌放入弃牌堆，返回 False
    如果一方胜利：触发进程中的 if 语句，返回 True
    '''
    # Before
    gameDrawCard(squad,cardNum=5) # draw cards to hand
    game.costNow = game.COSTLIMIT # refill the cost
    # During
    if gameAction(squad,game): # 仍会执行gameAction()，但其内含循环语句，且默认返回值为 False ，当且仅当游戏结束或主动结束游戏时其返回 True ，此时触发if语句并直接返回 True 。
        return True
    # After
    game.costNow = 0 # 以后可以添加默认保留费用的能力
    squad['discard'].extend(squad['hand']) # 以后可以添加未使用则消耗的卡牌
    squad['hand'].clear() # 以后可以添加可保留卡牌
    return False

def gameIsWin(game):
    '''由于entityList不移动，直接判断前两排（敌方）和后两排（我方）情况来确认胜负（列表长度之和为 0 则负）。'''
    if len(game.entityList['enemy'][0]) + len(game.entityList['enemy'][1]) == 0:
        print('我方胜利！')
    elif len(game.entityList['ally'][0]) + len(game.entityList['ally'][1]) == 0:
        print('敌方胜利！')
    else:
        return False
    return True

def gameRoutine():
    '''
    游戏核心进程。
    
    首先实例化全局游戏，变量 isEnd 设为 False 。
    进入循环，直到 gameIsWin() 返回结果 True 代表游戏结束，跳出循环。
    每回合翻转一次entityList以调整双方位置显示。（新变动）（暂时停用，与 gameIsWin() 适配有问题。）
    '''
    game = Game() # initialize
    isEnd = False
    while True:
        print('我方回合：')
        isEnd = gameTurn(game.allySquad,game)
        if isEnd == True:
            break
        # Game.entityList.reverse()
        loading()
        print('敌方回合：')
        isEnd = gameTurn(game.enemySquad,game)
        if isEnd == True:
            break
        # Game.entityList.reverse()
    