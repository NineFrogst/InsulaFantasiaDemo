from FeatureFuncs import *
from DataIO import *

# 编队界面
def PageSquad():
    print('-----------\n编 队 界 面\n-----------')
    print('[沙盒 模式]')
    print('1. 己方编辑\n2. 敌方编辑\n0. 返回前页')
    squadSelect = str(input("\n请选择页面："))
    if squadSelect == '1':
        squadAlly()
    elif squadSelect == '2':
        squadEnemy()

    return 2

# 己方队伍
def squadAlly():
    print('-----------\n己 方 编 辑\n-----------')
    print('1. 队伍编辑\n2. 卡组编辑\n0. 返回前页')
    allySelect = str(input("\n请选择页面："))
    if allySelect not in ['1','2']:
        PageSquad()
        return
    squadNow = eval(getSquad('ally'))
    if allySelect == '1':
        allyCharacter(squadNow)
    elif allySelect == '2':
        allyCard(squadNow)
def allyCharacter(squadNow):
    allyFront = [' ',' ',' ',' ',' ']
    allyBack = [' ',' ',' ',' ',' ']
    i = 0
    for cID in eval(squadNow['front']):
        charDict = getCharacterDB('np_find',cID)
        allyFront[i] = eval(charDict['info'])['abbr']
        i += 1
    i = 0
    for cID in eval(squadNow['back']):
        charDict = getCharacterDB('np_find',cID)
        allyBack[i] = eval(charDict['info'])['abbr']
        i += 1
    del i
    print('当前队伍：')
    print('前 {:<10} {:<10} {:<10} {:<10} {:<10}'.format(allyFront[0],allyFront[1],allyFront[2],allyFront[3],allyFront[4]))
    print('后 {:<10} {:<10} {:<10} {:<10} {:<10}'.format(allyBack[0],allyBack[1],allyBack[2],allyBack[3],allyBack[4]))
    print('　 {:<10} {:<10} {:<10} {:<10} {:<10}'.format('1','2','3','4','5'))

def allyCard():
    pass

# 敌方队伍
def squadEnemy():
    pass