import time

# 花里胡哨

# 伪缓冲
def loading():
    print("Loading......")
    time.sleep(1)

# 改变内存地址的拷贝/赋值
def cleancopy(item):
    itemstr = str(item)
    return eval(item)