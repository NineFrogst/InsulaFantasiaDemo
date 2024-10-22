# 正在查看源代码页面
from LibSys import *
version = "0.0.1.a001"
signal = 0
# 游戏内容

# 游戏界面
def PageGame():
    print("然而还没有做好啊")
    PageOpening()

# 编队界面
def PageSquad():
    print("然而还没有做好啊")
    PageOpening()




# 开始页面
def PageOpening():
    loading()
    
    # 基本信息
    print("---------------------\n|  INSULA FANTASIA  |\n---------------------")
    print("欢迎体验《幻岛缘游》卡牌游戏系统demo版！")
    print("当前版本：{}".format(version))
    print("\n1. 开始游戏\n2. 查看编队\n3. 查看图鉴\n4. 退出游戏")

    # page_select
    pageSelect = input("\n请输入数字以选择选项：")
    
    loading()
    global signal
    if pageSelect == '1':
        PageGame()
    elif pageSelect == '2':
        PageSquad()
    elif pageSelect == '3':
        signal = PageLibrary()



# main_function
PageOpening()
if signal == 3:
    if str(input('返回首页？（y/n）')) == 'n':
        PageLibrary()
    else:
        PageOpening()