# encoding: UTF-8

import time
from logging import INFO

########################################################################
class VtBaseData(object):
    """回调函数推送数据的基础类，其他数据类继承于此"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
 
########################################################################
class VtTickData(VtBaseData):
    """Tick行情数据类"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(VtTickData, self).__init__()
        
        # 代码相关
        self.symbol = "sh000001"              # 合约代码
        self.exchange = "sz000001"            # 交易所代码
        self.vtSymbol = "EMPTY_STRING"            # 合约在vt系统中的唯一代码，通常是 合约代码.交易所代码



