from FeatureFuncs import *
from DataIO import *

# 图鉴界面
def PageLibrary():
    # 选择图鉴
    print("图 鉴 选 择\n-----------\n1. 人物图鉴\n2. 卡牌图鉴\n0. 返回前页")
    libSelect = str(input("\n请选择页面："))
        
    if libSelect == '1':
        libCharacter()
    elif libSelect == '2':
        print('tbd')
    else:
        return 3

# 人物图鉴
def libCharacter():
    print("人 物 图 鉴\n-----------\n1. 所有人物\n2. 船员图鉴\n3. 敌方图鉴\n4. 其他角色\n0. 返回前页")
    libChrSelect = str(input("\n请选择页面："))
    loading()
    while True:
        if libChrSelect not in ['1','2','3','4']:
            PageLibrary()
            break
        if libChrSelect == '1':
            getCharacterDB('get')
        elif libChrSelect == '2':
            getCharacterDB('get','crews')
        elif libChrSelect == '3':
            getCharacterDB('get','hostiles')
        elif libChrSelect == '4':
            getCharacterDB('get','others')
        libChrAction()
        break
# 人物图鉴操作
def libChrAction():
    while True:
        print('1. 查找角色 2. 新建项目 3. 修改项目 4. 删除项目\n0. 返回前页')
        libChrAct = str(input('\n请选择操作：'))
        loading()
        if libChrAct == '1':
            lookID_ = str(input('所查找角色的ID：'))
            loading()
            getCharacterDB('find',lookID_)
        elif libChrAct == '2':
            newChrList = ['null','null','0','null','null']
            newChrList[0] = str(input('请输入新的角色ID：'))
            newChrList[1] = str(input('请输入新的角色名称：（英文）'))
            newChrList[2] = str(input('请输入稀有度：（1~3）'))
            newChrList[3] = str(input('请输入职业：'))
            newChrList[4] = str(input('请输入配音：'))
            # newChrList = [newID,newName,newRarity,newClass,newDubbing]
            loading()
            getCharacterDB('new',newChrList)
        elif libChrAct == '3':
            newChrList = ['null','null','0','null','null']
            newChrList[0] = str(input('请输入要修改的角色ID：'))
            newChrList[1] = str(input('请输入新的角色名称：（英文）'))
            newChrList[2] = str(input('请输入稀有度：（1~3）'))
            newChrList[3] = str(input('请输入职业：'))
            newChrList[4] = str(input('请输入配音：'))
            # newChrList = [newID,newName,newRarity,newClass,newDubbing]
            loading()
            getCharacterDB('edit',newChrList)
        elif libChrAct == '4':
            lookID_ = str(input('要删除角色的ID：'))
            loading()
            delChar = eval(getCharacterDB('find',lookID_))
            if str(input('是否删除 {} ？（y/n）'.format(delChar['name']))) == 'y':
                loading()
                getCharacterDB('del',lookID_)
                
        else:
            libCharacter()
            break