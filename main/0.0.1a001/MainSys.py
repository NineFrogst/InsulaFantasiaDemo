# 正在查看源代码页面
import time
version = "0.0.1.a001"

# 游戏内容

# 游戏界面
def PageGame():
    print("然而还没有做好啊")
    PageOpening()

# 编队界面
def PageSquad():
    print("然而还没有做好啊")
    PageOpening()

# 图鉴界面
def PageLibrary():
    print("然而还没有做好啊")
    PageOpening()

# 开始页面
def PageOpening():
    # 伪缓冲
    print("Loading......")
    time.sleep(1)

    # 基本信息
    print("---------------------\n|  INSULA FANTASIA  |\n---------------------")
    print("欢迎体验《幻岛缘游》卡牌游戏系统demo版！")
    print("当前版本：{}".format(version))
    print("\n1. 开始游戏\n2. 查看编队\n3. 图鉴\n4. 退出游戏")

    # page_select
    pageSelect = input("\n请输入数字以选择选项：")
    print("Loading......")
    time.sleep(1) # 伪缓冲
    if pageSelect == '1':
        PageGame()
    elif pageSelect == '2':
        PageSquad()
    elif pageSelect == '3':
        PageLibrary()


# main_function
PageOpening()