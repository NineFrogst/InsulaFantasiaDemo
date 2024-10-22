# 正在查看源代码页面
from GameSys import *
from SquadSys import *
from LibSys import *
version = "0.0.1.a008"
signal = 0

# 游戏内容

# 开始页面
def PageOpening():
    '''
    游戏开场页面。

    输入数字，分支到其他页面。
    同时接收分页面传来的signal信号（返回值）来显示不同的内容。

    TODO: 游戏教程与使用指南，防字符串注入（InjectionBlocker.py）。
    TODO: 有闲心了就开始埋彩蛋。
    '''
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
        signal = PageGame()
    elif pageSelect == '2':
        signal = PageSquad()
    elif pageSelect == '3':
        signal = PageLibrary()
    else:
        signal = 0

    return 0



# main_function

# 在盒子里（划掉）In case of 发行版中出现错误，请启用下方代码以代替下方原本的PageOpening()：
# try:
#     PageOpening()
# except:
#     print('发生错误，正在返回首页......')
#     PageOpening()
PageOpening()
while True: # signal的使用场景
    if signal == 0:
        break
    elif signal == 1:
        if str(input('重新开始？（y/n）')) == 'y':
            PageGame()
            break
    elif signal == 2:
        if str(input('返回首页？（y/n）')) == 'n':
            PageSquad()
            break
    elif signal == 3:
        if str(input('返回首页？（y/n）')) == 'n':
            PageLibrary()
            break
    PageOpening()