'''
该文件存储各项卡牌的实际实现函数。
函数名即为卡牌的id。（没错我又偷懒了）
'''

import random

def a9001(userObj,useeObj,game):
    return useeObj.takeATK(userObj,game,5)

def a9002(userObj,useeObj,game):
    damage=4
    if "guarded" in userObj.status:
        damage+=4
    useeObj.takeATK(userObj,game,damage,isPiercing=True)

def s9001(userObj,useeObj,game):
    pass

def a9003(userObj,useeObj,game):
    useeObj.takeATK(userObj,game,2)

def s9002(userObj,useeObj,game):
    userObj.takeDEF(userObj,game,4)

def s9003(userObj,useeObj,game):
    if userObj.side == useeObj.side:
        useeObj.takeEffect(game,"guarded",dataList=[2,userObj])

def a9004(userObj,useeObj,game):
    useeObj.takeEffect(game,"poison",dataList=[3,userObj])

def a9005(userObj,useeObj,game):
    useeObj.takeATK(userObj,game,3)
    useeObj.takeEffect(game,"poison",dataList=[1,userObj])

def s9004(userObj,useeObj,game):
    if userObj.cID != "c903" \
    and useeObj.situation == "attacked":
        userObj.takeEffect(game,"weakness",dataList=[1,useeObj])

def a9006(userObj,useeObj,game):
    useeObj.takeATK(userObj,game,random.choice([1,1,1,1,6]))

def s9005(userObj,useeObj,game):
    useeObj.takeHEL(userObj,game,4)

def s9006(userObj,useeObj,game):
    for row in game.entityList[{"ally":"enemy","enemy":"ally"}[userObj.side]]:
        for useeObj in row:
            useeObj.takeEffect(game,"poison",dataList=[2,userObj])

def s9007(userObj,useeObj,game):
    for row in game.entityList[userObj.side]:
        for useeObj in row:
            useeObj.takeDEF(userObj,game,1)

def a9007(userObj,useeObj,game):
    if userObj.cID != "c902" \
    and useeObj.situation == "attacked" \
    and userObj not in game.entityList[useeObj.side][0] \
    and userObj not in game.entityList[useeObj.side][1] \
    and random.randint(0,1):
        userObj.takeATK(useeObj,game,2)


def cardHandler(kID:int):
    if kID in globals():
        handler:function = globals()[kID]
        return handler
    else:
        print('卡牌效果未找到。')
        def error(*args,**kwargs):
            return
        return error