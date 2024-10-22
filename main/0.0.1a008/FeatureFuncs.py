'''
花里胡哨
'''

import time

# 伪缓冲
def loading():
    print("Loading......")
    time.sleep(1)

# 改变内存地址的拷贝/赋值（不算深拷贝）
def cleancopy(item):
    itemstr = str(item)
    return eval(item)