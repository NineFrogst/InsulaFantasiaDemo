'''
各种状态效果及其对应的函数。
'''

def effectPoison(charObj:object,game,effectData:list,args):
    charObj.takeDamage(effectData[1],game,effectData[0])

def effectGuarded(charObj,game,effectData,args):
    cardPlayList = args[0] # [userObj,useeObj,cardDict]
    if cardPlayList[1] == charObj \
    and cardPlayList[0].side != charObj.side \
    and (effectData[1] in game.entityList[charObj.side][0] or effectData[1] in game.entityList[charObj.side][1]) \
    and eval(cardPlayList[2]['info'])['area'] != 'side':
        cardPlayList[1] = effectData[1]

def effectWeakness(charObj,game,effectData,args):
    charObj.ratio['ATK'][0].append(-0.5)



effectMap:dict = {
    'poison': {
        'eventListener': 'roundStart',
        'description': 'Cause layers amount of damage every round.',
        'timewise': True,
        'add': True,
        'action': effectPoison
    },
    'guarded':{
        'eventListener': 'cardStart',
        'description': 'Transfer damage to the guardian.',
        'timewise': True,
        'add': False,
        'action': effectGuarded
    },
    'weakness':{
        'eventListener': 'cardStart',
        'description': 'Lower one\'s attack by 50%.',
        'timewise': True,
        'add': True,
        'action': effectWeakness
    },
}