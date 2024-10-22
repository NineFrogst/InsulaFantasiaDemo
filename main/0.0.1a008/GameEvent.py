'''
为了便于设计并使用花里胡哨的卡牌，也为了理清游戏进程，同时考虑到不往一个文件里堆料太多，单开一个模块，主管游戏事件。
'''

from DataIO import *
import Effects


class Event:
    __eventListeners:list = ['gameOpening','roundStart', 'handDraw', 'cardStart', 'cardPlay', 'cardEnd','roundEnd']
    __effectMap:dict =  Effects.effectMap

    def __init__(self,game:object):
        self.game = game
        game.event = self
        def event_subscriber(kID):
            cardDict = getCardDB('find',kID)
            kPpty = eval(cardDict['ppty'])
            self.subscribe(kPpty['listener'],userObj,kID)
        for side in game.entityList:
            for row in game.entityList[side]:
                for userObj in row:
                    if 'passive' not in userObj.cPpty:
                        continue
                    if ',' in userObj.cPpty['passive'] :
                        for kID in eval(userObj.cPpty['passive']):
                            event_subscriber(kID)
                    else:
                        event_subscriber(userObj.cPpty['passive'])

    def subscribe(self,listener:str,charObj:object,kID:str):
        if listener not in Event.__eventListeners:
            return print('Listener not exists.')
        if listener not in list(charObj.events.values()):
            charObj.events[listener] = []
        charObj.events[listener].append(kID)
    
    def unsubscribe(self,listener,charObj,kID=None):
        if listener not in list(charObj.events.values()):
            return
        if kID == None:
            charObj.events[listener].clear()
            return
        if kID not in charObj.events[listener]:
            return
        charObj.events[listener].remove(kID)

    def publish(self,listener:str,data):
        if listener == 'gameOpening':
            self.__gOhandler(data)
        elif listener == 'roundStart':
            self.__rSEhandler('roundStart',data)
        elif listener == 'handDraw':
            self.__hDhandler(data)
        elif listener == 'cardStart':
            self.__cSEhandler('cardStart',data)
        elif listener == 'cardPlay':
            self.__cPhandler(data)
        elif listener == 'cardEnd':
            self.__cSEhandler('cardEnd',data)
        elif listener == 'roundEnd':
            self.__rSEhandler('roundEnd',data)

    def __gOhandler(self,entityList:dict):
        game: object = self.game
        for side in list(entityList.values()):
            for row in side:
                for userObj in row:
                    for kID in userObj.events['gameOpening']:
                        Cards.cardHandler(kID)(userObj,userObj,game)
                    self.statusHandler('gameOpening',userObj)
    def __rSEhandler(self,mode:str,side: list):
        game: object = self.game
        for row in side:
            for userObj in row:
                for kID in userObj.events[mode]:
                    Cards.cardHandler(kID)(userObj,userObj,game)
                self.statusHandler(mode,userObj)
    def __cSEhandler(self,mode:str,data:list):
        game: object = self.game
        userObj:object = data[0]
        useeObj:object = data[1]
        cardDict = data[2]
        kID = cardDict['id']
        userAction: list = []
        useeAction: list = []
        cP_break1: None = None
        cP_break2: None = None
        for passiveID in userObj.events[mode]:
            userAction.append(Cards.cardHandler(passiveID))
        for passiveID in useeObj.events[mode]:
            useeAction.append(Cards.cardHandler(passiveID))
        if mode == 'cardStart':
            if kID[0] == 'a':
                userObj.situation = 'attacking'
                useeObj.situation = 'attacked'
            for passive in userAction:
                cP_break1 = cP_break1 or passive(userObj,useeObj,game)
            cP_break1 = cP_break1 or self.statusHandler(mode,userObj,data)
            for passive in useeAction:
                cP_break2 = cP_break2 or passive(userObj,useeObj,game) 
            cP_break2 = cP_break2 or self.statusHandler(mode,useeObj,data)
            # print('Situations: ',userObj.situation,' and ',useeObj.situation)
        elif mode == 'cardEnd':
            for passive in useeAction:
                passive(userObj,useeObj,game)
            self.statusHandler(mode,useeObj,data)
            for passive in userAction:
                passive(userObj,useeObj,game)
            self.statusHandler(mode,userObj,data)
            userObj.situation = None
            useeObj.situation = None
            userObj.ratio = {'ATK' : [[0],[0]], 'DEF' : [[0],[0]], 'HEL' : [[0],[0]]}
            useeObj.ratio = {'ATK' : [[0],[0]], 'DEF' : [[0],[0]], 'HEL' : [[0],[0]]}

        if cP_break1 or cP_break2:
            return True # 这里True了之后会跳过卡牌的生效
    def __cPhandler(self,data:list):
        game: object = self.game
        userObj = data[0]
        useeObj = data[1]
        cardDict = data[2]
        print('{} 对 {} 使用了 {} ！'.format(userObj.cName,useeObj.cName,cardDict['name']))
        self.statusHandler('cardPlay',userObj)
        self.statusHandler('cardPlay',useeObj)
        Cards.cardHandler(cardDict['id'])(userObj,useeObj,game)
    def __hDhandler(self,entityList):
        game: object = self.game
        pass

    def statusHandler(self,listener,charObj,*args):
        popEffect = []
        value = None
        for effect in charObj.status:
            if Event.__effectMap[effect]['eventListener'] != listener:
                continue
            value = value or Event.__effectMap[effect]['action'](charObj, self.game, charObj.status[effect], list(args))
            if listener == 'roundStart' and Event.__effectMap[effect]['timewise']:
                charObj.status[effect][0] -= 1
            if charObj.status[effect][0] <= 0:
                popEffect.append(effect)
                continue
        for effect in popEffect:
            charObj.status.pop(effect)
        return value
