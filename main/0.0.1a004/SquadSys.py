from FeatureFuncs import *
from DataIO import *

# 编队界面
def PageSquad():
    print('-----------\n编 队 界 面\n-----------')
    print('[ 沙 盒 模 式 ]') # 因为现在确实是沙盒模式
    print('1. 己方编辑\n2. 敌方编辑\n0. 返回前页')
    squadSelect = str(input("\n请选择页面："))
    if squadSelect == '1':
        squadAlly()
    elif squadSelect == '2':
        squadEnemy()

    return 2

# 人物编队（无论敌我，反正没区别参数都用'ally'了）
def squadChrPrint(squadNow):
    squadFront = [' ',' ',' ',' ',' ']
    squadBack = [' ',' ',' ',' ',' ']
    i = 0
    for cID in eval(squadNow['front']):
        charDict = getCharacterDB('np_find',cID)
        squadFront[i] = eval(charDict['info'])['abbr']
        i += 1
    i = 0
    for cID in eval(squadNow['back']):
        charDict = getCharacterDB('np_find',cID)
        squadBack[i] = eval(charDict['info'])['abbr']
        i += 1
    del i
    print('前 {:<10} {:<10} {:<10} {:<10} {:<10}'.format(squadFront[0],squadFront[1],squadFront[2],squadFront[3],squadFront[4]))
    print('后 {:<10} {:<10} {:<10} {:<10} {:<10}'.format(squadBack[0],squadBack[1],squadBack[2],squadBack[3],squadBack[4]))
    print('　 {:<10} {:<10} {:<10} {:<10} {:<10}'.format('1','2','3','4','5'))
    return squadNow
def squadCharacter(squadNow):
    print('当前队伍：')
    squadChrPrint(squadNow)
    return squadChrAction(squadNow)

def squadChrAction(squadNow): # 前方跳跃很有用
    print('1. 修改编队 2. 保存预设 3. 查看预设\n0. 返回前页')
    squadChrAct = str(input('请选择操作：'))
    loading()
    if squadChrAct == '1':
        newFront = []
        newBack = []
        for i in range(5):
            char = str(input('（录入结束请留空按回车）\n请输入新的前排角色ID：'))
            if char == '':
                break 
            newFront.append(char)
        if len(newFront) == 0:
            print('前排至少安排一名角色！')
            return squadChrAction(squadNow)
        for i in range(5):
            char = str(input('（结束请留空按回车）\n请输入新的后排角色ID：'))
            if char == '':
                break 
            newBack.append(char)
        if (len(newFront) + len(newBack)) > 4:
            if str(input('当前编队超过 4 人，是否保存？（y/n）')) == 'n':
                return squadChrAction(squadNow)
        loading()
        squadNow['front'] = str(newFront)
        squadNow['back'] = str(newBack)
        getSquad('ally','edit',squadNow)
        print('编队修改已保存。')
    elif squadChrAct == '2':
        newPreset = str(input('为该预设命名：'))
        if newPreset == '':
            print('未设置名称。')
        elif newPreset in list(getSquad('ally','get').keys()):
            loading()
            if str(input('预设名已存在，是否覆盖？（y/n）')) == 'y':
                squadNow['preset'] = newPreset
                getSquad('ally','edit',squadNow)
        else:
            loading()
            squadNow['preset'] = newPreset
            getSquad('ally','new',squadNow)
    elif squadChrAct == '3':
        while True:
            squadDict = getSquad('ally','get')
            print('预设列表：')
            j = 1
            for i in list(squadDict.keys()):
                print(f'{j:>2}. {i:<}')
                j+=1
            del j
            presetSelect = str(input('选择预设（数字）：'))
            loading()
            if presetSelect in [str(i) for i in range(1,len(list(squadDict.keys()))+1)]:
                lookPreset = eval(list(squadDict.values())[eval(presetSelect)-1])
                print('预设队伍：')
                squadChrPrint(lookPreset)
            else:
                print('未找到预设，退出中......')
                break
            print('1. 适用 2. 修改 3. 删除 0. 退出')
            presetAct = str(input('请选择操作：'))
            loading()
            if presetAct == '1':
                lookPreset['preset'] = squadNow['preset']
                squadNow = getSquad('ally','edit',lookPreset)
                break
            elif presetAct == '2':
                newFront = []
                newBack = []
                for i in range(5):
                    char = str(input('（结束请留空按回车）\n请输入新的前排角色ID：'))
                    if char == '':
                        break 
                    newFront.append(char)
                if len(newFront) == 0:
                    print('前排至少安排一名角色！')
                    continue
                for i in range(5):
                    char = str(input('（结束请留空按回车）\n请输入新的后排角色ID：'))
                    if char == '':
                        break 
                    newBack.append(char)
                if (len(newFront) + len(newBack)) > 4:
                    if str(input('当前编队超过 4 人，是否保存？（y/n）')) == 'n':
                        continue
                loading()
                lookPreset['front'] = str(newFront)
                lookPreset['back'] = str(newBack)
                getSquad('ally','edit',lookPreset)
                print('预设修改已保存。')
            elif presetAct == '3':
                if str(input(f'确认删除 {lookPreset["preset"]} ？（y/n）')) == 'y':
                    loading()
                    getSquad('ally','del',lookPreset['preset'])
                    break
                continue
            break
    # 是屎山啊！！纯纯的屎山啊！！！嘲笑屎山理解屎山成为屎山（悲）主要是我真的不想为了这用一次的东西开个函数了，文笔也就这样，有能力和想法再改
    else:
        return
    return squadCharacter(squadNow)
            
            
def squadCard(squadNow):
    squadDeck = eval(squadNow['cardset'])
    print('当前卡组：')
    for i in range(len(squadDeck)):
        kName = getCardDB('np_find',squadDeck[i])['name']
        print(f'{str(i+1):>2}. {kName:<}')
    print('1. 增加卡牌 2. 删除卡牌 0. 返回前页\n注：卡组与队伍预设绑定，切换预设将切换卡组。')
    squadCrdAct = str(input('请选择操作：'))
    loading()
    if squadCrdAct == '1':
        newCard = getCardDB('np_find',str(input('请输入添加的卡牌ID：')))
        loading()
        squadDeck.append(newCard['id'])
        squadNow['cardset'] = str(squadDeck)
        getSquad('ally','edit',squadNow)
        print('{} 添加成功。'.format(newCard['name']))
    elif squadCrdAct == '2':
        delCard = str(input('请输入删除的卡牌序号（数字）：'))
        loading()
        if delCard in [str(i) for i in range(1,len(squadDeck)+1)]:
            delkName = getCardDB('np_find',squadDeck[eval(delCard)-1])['name']
            if str(input(f'确认删除 {delkName} ？（y/n）')) == 'y':
                loading()
                squadDeck.pop(eval(delCard)-1)
                squadNow['cardset'] = str(squadDeck)
                getSquad('ally','edit',squadNow)
                print(f'{delkName} 删除成功。')
    else:
        return
    return squadCard(squadNow)

# 己方队伍
def squadAlly():
    print('-----------\n己 方 编 辑\n-----------')
    print('1. 队伍编辑\n2. 卡组编辑\n0. 返回前页')
    allySelect = str(input("\n请选择页面："))
    loading()
    if allySelect not in ['1','2']:
        PageSquad()
        return
    squadNow = eval(getSquad('ally'))
    if allySelect == '1':
        squadCharacter(squadNow)
    elif allySelect == '2':
        squadCard(squadNow)
    return squadAlly()
# 敌方队伍
def squadEnemy():
    print('-----------\n敌 方 编 辑\n-----------')
    print('1. 队伍编辑\n2. 卡组编辑\n0. 返回前页')
    enemySelect = str(input("\n请选择页面："))
    loading()
    if enemySelect not in ['1','2']:
        PageSquad()
        return
    squadNow = eval(getSquad('enemy'))
    if enemySelect == '1':
        squadCharacter(squadNow)
    elif enemySelect == '2':
        squadCard(squadNow)
    return squadEnemy()