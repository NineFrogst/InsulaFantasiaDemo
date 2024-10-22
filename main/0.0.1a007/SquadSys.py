from FeatureFuncs import *
from DataIO import *

# 编队界面
def PageSquad():
    '''
    编队界面的主界面。

    可以查看并编辑己方的编队及牌组。
    [沙盒模式]：可以分别查看并编辑己方和敌方的编队及牌组。
    修改的内容将会在游戏（PageGame()）时体现。

    TODO: 代码整理重构 *done*
    '''
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
    """
    打印编队组成。

    先定义两个长度5，元素全为空字符串的列表squadFront和squadBack，代表前排角色和后排角色。
    随后从传入的字典squadNow中，读取front和back的内容，并以其中的cID为索引，查找对应角色的名称缩写。
    将缩写放入两个列表的对应位置，释放i的空间，然后格式化并输出。

    传入的字典squadNow不同，输出的内容也不同，故可以接受任意来源的字典，且没有特异的输出内容。
    """
    squadFront = [' ',' ',' ',' ',' ']
    squadBack = [' ',' ',' ',' ',' ']
    i = 0
    for cID in eval(squadNow['front']):
        charDict = getCharacterDB('find',cID)
        squadFront[i] = eval(charDict['info'])['abbr']
        i += 1
    i = 0
    for cID in eval(squadNow['back']):
        charDict = getCharacterDB('find',cID)
        squadBack[i] = eval(charDict['info'])['abbr']
        i += 1
    del i
    print('__|{:_<10}|{:_<10}|{:_<10}|{:_<10}|{:_<10}|'.format('1','2','3','4','5'))
    print('前|{:<10} {:<10} {:<10} {:<10} {:<10}'.format(squadFront[0],squadFront[1],squadFront[2],squadFront[3],squadFront[4]))
    print('后|{:<10} {:<10} {:<10} {:<10} {:<10}'.format(squadBack[0],squadBack[1],squadBack[2],squadBack[3],squadBack[4]))
    print('--|{:-<10}|{:-<10}|{:-<10}|{:-<10}|{:-<10}|'.format('','','','',''))
    return squadNow

def squadCharacter(squadNow): # 前方跳跃很有用
    '''
    人物编队操作。

    ~~！！！注意！！！该代码非常屎山，维护成本极高，要是我现在不把注释写清楚，之后维护我自己也看不懂！！~~
    注：屎山已修，不同功能部件已经拆散，更方便理解和查阅，倒是没有太多逻辑上的改动。

    打印当前编队→提供增删改查操作
    修改编队：创建新的空前后排列表，录入角色（循环最多五次，即一排五个角色），由于按照游戏规则，编队最多四人，添加判断语句。
    保存预设：命名现在的编队并保存在文件中。
    沙盒模式下，角色编队超四人不会强制阻止录入。

    查看预设：查看预设列表并选择，选择未找到则自动返回前页。
    适用：将所查看预设覆盖到当前预设中，并返回当前编队页。
    修改：同修改编队。
    删除：将该名称对应的编队删除。
    由于我方编队与敌方编队也以t00、r00的名称保存在文件中，查找时将跳过以免误操作。（新变动）

    TODO: 尝试把部分代码放入DataIO.py，优化代码结构。*done*
    '''
    while True:
        print('当前队伍：')
        squadChrPrint(squadNow)
        if squadChrAction(squadNow):
            break
def squadChrAction(squadNow):
    '''
    用来降低嵌套程度，美化代码而分离出来的函数，详见squadCard()。
    '''
    def squadChrEdit():
        newFront = []
        newBack = []
        for i in range(5):
            char = str(input('（录入结束请留空按回车）\n请输入新的前排角色ID：'))
            if char == '':
                break 
            newFront.append(char)
        if len(newFront) == 0:
            print('前排至少安排一名角色！')
            return False
        for i in range(5):
            char = str(input('（结束请留空按回车）\n请输入新的后排角色ID：'))
            if char == '':
                break 
            newBack.append(char)
        if (len(newFront) + len(newBack)) > 4:
            if str(input('当前编队超过 4 人，是否保存？（y/n）')) == 'n':
                return False
        loading()
        squadNow['front'] = str(newFront)
        squadNow['back'] = str(newBack)
        getSquad('ally','edit',squadNow)
        print('编队修改已保存。')
        return True
    def squadChrSave():
        newPreset = str(input('为该预设命名：'))
        if newPreset == '':
            print('未设置名称。')
            return False
        loading()
        if newPreset not in list(getSquad('ally','get').keys()):
            squadNow['preset'] = newPreset
            getSquad('ally','new',squadNow)
        elif str(input('预设名已存在，是否覆盖？（y/n）')) == 'y':
            squadNow['preset'] = newPreset
            getSquad('ally','edit',squadNow)
        return False
    def squadChrGet():
        while True:
            squadDict = getSquad('ally','get')
            squadDict.pop('t00')
            squadDict.pop('r00')
            print('预设列表：')
            squadKeyList = list(squadDict.keys())
            for i in range(len(squadKeyList)):
                print('{:>2}. {:<}'.format(i+1,squadKeyList[i]))
            if presetSelection(squadDict):
                return False

    print('1. 修改编队 2. 保存预设 3. 查看预设\n0. 返回前页')
    squadChrAct = str(input('请选择操作：'))
    loading()
    if squadChrAct == '1':
        return squadChrEdit()
    elif squadChrAct == '2':
        return squadChrSave()
    elif squadChrAct == '3':
        return squadChrGet()
    return True
def presetSelection(squadDict):
    '''
    用来降低嵌套程度，美化代码而分离出来的函数，详见squadCharacter()。
    '''
    presetSelect = str(input('选择预设（数字）：'))
    loading()
    if presetSelect in [str(i) for i in range(1,len(list(squadDict.keys()))+1)]:
        lookPreset = eval(list(squadDict.values())[eval(presetSelect)-1])
        print('预设队伍：')
        squadChrPrint(lookPreset)
    else:
        print('未找到预设，退出中......')
        return True
    print('1. 适用 2. 修改 3. 删除 0. 退出')
    presetAct = str(input('请选择操作：'))
    loading()
    if presetAct == '1':
        lookPreset['preset'] = squadNow['preset']
        squadNow = getSquad('ally','edit',lookPreset)
        return True
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
            return False
        for i in range(5):
            char = str(input('（结束请留空按回车）\n请输入新的后排角色ID：'))
            if char == '':
                break 
            newBack.append(char)
        if (len(newFront) + len(newBack)) > 4:
            if str(input('当前编队超过 4 人，是否保存？（y/n）')) == 'n':
                return False
        loading()
        lookPreset['front'] = str(newFront)
        lookPreset['back'] = str(newBack)
        getSquad('ally','edit',lookPreset)
        print('预设修改已保存。')
    elif presetAct == '3':
        if str(input(f'确认删除 {lookPreset["preset"]} ？（y/n）')) != 'y':
            print('已取消删除。')
            return False
        loading()
        getSquad('ally','del',lookPreset['preset'])
    return True



def squadCard(squadNow):
    '''
    打印编队卡组。

    编队卡组与编队绑定，如果切换预设是覆盖了编队，卡组会一并覆盖。
    同样可以实现卡组内卡牌的增删补查。
    想要修改某一预设的卡组，可以按照以下流程：选择预设覆盖编队→退出队伍编辑，打开卡组编辑→修改卡组，退出卡组编辑，打开队伍编辑→保存预设，覆盖原有预设或保存为新预设
    '''
    while True:
        squadDeck = eval(squadNow['cardset'])
        print('当前卡组：')
        for i in range(len(squadDeck)):
            kName = getCardDB('find',squadDeck[i])['name']
            print(f'{str(i+1):>2}. {kName:<}')
        if squadCrdAction(squadNow,squadDeck):
            break
def squadCrdAction(squadNow,squadDeck):
    '''
    用来降低嵌套程度，美化代码而分离出来的函数，详见squadCard()。
    '''
    print('1. 增加卡牌 2. 删除卡牌 0. 返回前页\n注：卡组与队伍预设绑定，切换预设将切换卡组。')
    squadCrdAct = str(input('请选择操作：'))
    loading()
    if squadCrdAct == '1':
        newCard = getCardDB('find',str(input('请输入添加的卡牌ID：')))
        loading()
        squadDeck.append(newCard['id'])
        squadNow['cardset'] = str(squadDeck)
        getSquad('ally','edit',squadNow)
        print('{} 添加成功。'.format(newCard['name']))
    elif squadCrdAct == '2':
        delCard = str(input('请输入删除的卡牌序号（数字）：'))
        loading()
        if delCard not in [str(i) for i in range(1,len(squadDeck)+1)]:
            print('未找到卡牌。')
            return False
        delkName = getCardDB('find',squadDeck[eval(delCard)-1])['name']
        if str(input(f'确认删除 {delkName} ？（y/n）')) != 'y':
            print('已取消删除。')
            return False
        loading()
        squadDeck.pop(eval(delCard)-1)
        squadNow['cardset'] = str(squadDeck)
        getSquad('ally','edit',squadNow)
        print(f'{delkName} 删除成功。')
    else:
        return True
    return False

# 己方队伍
def squadAlly():
    '''
    己方编辑页面。

    可选择队伍编辑或卡组编辑。
    '''
    while True:
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
# 敌方队伍
def squadEnemy():
    '''
    己方编辑页面。

    可选择队伍编辑或卡组编辑。
    '''
    while True:
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