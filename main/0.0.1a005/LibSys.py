from FeatureFuncs import *
from DataIO import *

# 图鉴界面
def PageLibrary():
    # 选择图鉴
    print("-----------\n图 鉴 选 择\n-----------\n1. 人物图鉴\n2. 卡牌图鉴\n0. 返回前页")
    libSelect = str(input("\n请选择页面："))
        
    if libSelect == '1':
        libCharacter()
    elif libSelect == '2':
        libCard()
        
    return 3

# 人物图鉴
def libCharacter():
    print("-----------\n人 物 图 鉴\n-----------\n1. 所有人物\n2. 船员图鉴\n3. 敌方图鉴\n4. 其他角色\n0. 返回前页")
    libChrSelect = str(input("\n请选择页面："))
    loading()
    if libChrSelect not in ['1','2','3','4']:
        PageLibrary()
        return

    getCharacterDB('get',[None,'c','h','o'][eval(libChrSelect)-1])
    return libChrAction()
# 人物图鉴操作
def libChrAction():
    print('1. 查找角色 2. 新建项目 3. 修改项目 4. 删除项目\n0. 返回前页')
    libChrAct = str(input('\n请选择操作：'))
    loading()
    if libChrAct == '1':
        header = ['id','name','稀有度','组别','职业']
        lookID = str(input('所查找角色的ID：'))
        loading()
        charDict = getCharacterDB('find',lookID)
        cID = eval(charDict)['id']
        cName = eval(charDict)['name']
        cGroup = eval(charDict)['group']
        try:
            cRarity = '☆'*eval(eval(eval(charDict)['info'])['rarity'])
            cSp = eval(eval(charDict)['info'])['class']
        except:
            cRarity = 'null'
            cSp = 'null'
        print('{:<5} {:<15} {:　<3} {:<6} {:<}'.format(header[0],header[1],header[2],header[3],header[4]))
        print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(cID,cName,cRarity,cGroup,cSp))
    elif libChrAct == '2':
        newChrList = ['null','null','null','null']
        newChrList[0] = str(input('请输入新的角色ID：'))
        newChrList[1] = str(input('请输入新的角色名称：（英文）'))
        newChrList[2] = {}
        newChrList[3] = {}
        newChrList[2]['rarity'] = str(input('请输入稀有度：（1~3）'))
        newChrList[2]['class'] = str(input('请输入职业：'))
        newChrList[2] = str(newChrList[2])
        
        loading()
        getCharacterDB('new',newChrList)
    elif libChrAct == '2+':
        newChrList = ['null','null',{},{}]
        newChrList[0] = str(input('cID='))
        newChrList[1] = str(input('cName='))
        newChrList[2] = str(input('cInfo='))
        newChrList[3] = str(input('cPpty='))
        loading()
        getCharacterDB('new',newChrList)
    elif libChrAct == '3':
        newChrList = ['null','null','null','null']
        newChrList[0] = str(input('请输入要修改的角色ID：'))
        newChrList[1] = str(input('请输入新的角色名称：（英文）'))
        newChrList[2] = {}
        newChrList[3] = {}
        newChrList[2]['rarity'] = str(input('请输入稀有度：（1~3）'))
        newChrList[2]['class'] = str(input('请输入职业：'))
        newChrList[2] = str(newChrList[2])
        
        loading()
        getCharacterDB('edit',newChrList)
    elif libChrAct == '3+':
        newChrList = ['null','null',{},{}]
        newChrList[0] = str(input('cID='))
        newChrList[1] = str(input('cName='))
        newChrList[2] = str(input('cInfo='))
        newChrList[3] = str(input('cPpty='))
        loading()
        getCharacterDB('edit',newChrList)
    elif libChrAct == '4':
        lookID = str(input('要删除角色的ID：'))
        loading()
        delChar = eval(getCharacterDB('find',lookID))
        if str(input('是否删除 {} ？（y/n）'.format(delChar['name']))) == 'y':
            loading()
            getCharacterDB('del',lookID)
    else:
        return libCharacter()
    return libChrAction()
            
# 卡牌图鉴
def libCard():
    print("-----------\n卡 牌 图 鉴\n-----------\n1. 所有卡牌\n2. 攻击卡牌\n3. 支援卡牌\n4. 召唤卡牌\n0. 返回前页")
    libCrdSelect = str(input("\n请选择页面："))
    loading()
    if libCrdSelect not in ['1','2','3','4']:
        PageLibrary()
        return

    getCardDB('get',[None,'a','s','m'][eval(libCrdSelect)-1])
    return libCrdAction()
# 卡牌图鉴操作
def libCrdAction():
    print('1. 查找卡牌 2. 新建项目 3. 修改项目 4. 删除项目\n0. 返回前页')
    libCrdAct = str(input('\n请选择操作：'))
    loading()
    if libCrdAct == '1':
        header = ['id','name','稀有度','组别','使用者']
        lookID = str(input('所查找卡牌的ID：'))
        loading()
        cardDict = getCardDB('find',lookID)
        kID = eval(cardDict)['id']
        kName = eval(cardDict)['name']
        kGroup = eval(cardDict)['group']
        try:
            kRarity = ['Bronze','Silver','Gold'][eval(eval(eval(cardDict)['info'])['rarity']) - 1]
            kSp = eval(eval(cardDict)['info'])['userID']
        except:
            kRarity = 'null'
            kSp = 'null'
        print('{:<5} {:<15} {:　<3} {:<6} {:<}'.format(header[0],header[1],header[2],header[3],header[4]))
        print('{:<5} {:<15} {:<6} {:<8} {:<}'.format(kID,kName,kRarity,kGroup,kSp))
    elif libCrdAct == '2':
        newCrdList = ['null','null','null','null']
        newCrdList[0] = str(input('请输入新的卡牌ID：'))
        newCrdList[1] = str(input('请输入新的卡牌名称：（英文）'))
        newCrdList[2] = {}
        newCrdList[3] = {}
        newCrdList[2]['rarity'] = str(input('请输入稀有度：（1~3）'))
        newCrdList[2]['userID'] = str(input('请输入使用者：'))
        newCrdList[2] = str(newCrdList[2])
        
        loading()
        getCardDB('new',newCrdList)
    elif libCrdAct == '2+':
        newCrdList = ['null','null','null','null']
        newCrdList[0] = str(input('kID='))
        newCrdList[1] = str(input('kName='))
        newCrdList[2] = str(input('kInfo='))
        newCrdList[3] = str(input('kPpty='))
        loading()
        getCardDB('new',newCrdList)
    elif libCrdAct == '3':
        newCrdList = ['null','null','null','null']
        newCrdList[0] = str(input('请输入要修改的卡牌ID：'))
        newCrdList[1] = str(input('请输入新的卡牌名称：（英文）'))
        newCrdList[2] = {}
        newCrdList[3] = {}
        newCrdList[2]['rarity'] = str(input('请输入稀有度：（1~3）'))
        newCrdList[2]['userID'] = str(input('请输入使用者：'))
        newCrdList[2] = str(newCrdList[2])

        loading()
        getCardDB('edit',newCrdList)
    elif libCrdAct == '3+':
        newCrdList = ['null','null','null','null']
        newCrdList[0] = str(input('kID='))
        newCrdList[1] = str(input('kName='))
        newCrdList[2] = str(input('kInfo='))
        newCrdList[3] = str(input('kPpty='))
        loading()
        getCardDB('edit',newCrdList)
    elif libCrdAct == '4':
        lookID_ = str(input('要删除卡牌的ID：'))
        loading()
        delCard = eval(getCharacterDB('find',lookID_))
        if str(input('是否删除 {} ？（y/n）'.format(delCard['name']))) == 'y':
            loading()
            getCharacterDB('del',lookID_)
    else:
        return libCard()
    return libCrdAction()