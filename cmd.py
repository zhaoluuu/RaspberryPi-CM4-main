import time
from xgolib import XGO
from xgoedu import XGOEDU
import random

# 初始化机器狗和头部控制接口
xgo = XGO("daxgolite")
XGO_edu = XGOEDU()

# 前进

# 撒尿

# 趴下
xgo.action(1, wait=True) # 趴下的id为1


# 复位机器狗，准备下一个动作
xgo.reset()
