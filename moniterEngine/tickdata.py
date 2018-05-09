from PyQt5.QtCore import *

from .eventEngine import *
import easyquotation
from .vtEvent import *
from collections import OrderedDict
from moniterEngine.saveData import *
import re
class MarketDataThread(QThread):
    def __init__(self, eventEngine):
        super(MarketDataThread, self).__init__()
        """Constructor"""
        self.eventEngine = eventEngine
        print("MarketDataThread")
        # 事件引擎开关
        self.__active = True
        self.ztDataCount =0

        self.quotation = easyquotation.use('sina')

    def setGateway(self,gw):
        if gw == "sina":
            print("set sina")
            self.quotation = easyquotation.use('sina')
        elif gw == "qq":
            print("set qq")
            self.quotation = easyquotation.use('qq')

    def run(self):
        while self.__active == True:
            try:
                self.processQuote()
                self.sleep(3)
            except Empty:
                pass


    def processQuote(self):
        tick = self.quotation.market_snapshot(prefix=True)
        self.onTick(tick)

    def dict_get(self,dictionary, cmd, default=None):
        cmd_list = cmd.split('.')
        tmp = dict(dictionary)
        for c in cmd_list:
            try:
                val = tmp.get(c, None)
            except AttributeError:
                return default
            if val != None:
                tmp = val
            else:
                return default
        return tmp

    def onTick(self, tick):
        """市场行情推送"""
        print(len(tick))
        custList1 = storeRecord("cust1")
        list = custList1.dataLoad()
        if(list == None):
            list=[]
        PlanAList = list[0]
        PlanCustList = ["300251", "600222", "300333"]
        self.ztDataCount =0
        self.dtDataCount =0
        for code in tick:
            close = self.dict_get(tick[code], 'close')
            now = self.dict_get(tick[code], 'now')

            if close != 0:
                zf = (now - close) / close
            else:
                zf = 0
            tick[code]['amount'] = zf
            ret = self.ztCount(close, now)
            if (ret == True and zf>0.06):
                self.ztDataCount += 1
            ret = self.dtCount(close, now)
            if(ret == True and zf<-0.04):
                self.dtDataCount += 1

            res = self.stockFilter(code)
            if(res == False):
                 tick[code]["valid"] = False
            else:
                tick[code]["valid"] = True
            res = self.setPlanList(code[2:],PlanAList)
            if (res == False):
                tick[code]["planA"] = False
            else:
                tick[code]["planA"] = True
            res = self.setPlanList(code[2:],PlanCustList)
            if (res == False):
                tick[code]["planCust"] = False
            else:
                tick[code]["planCust"] = True
        print("zhangting:")
        print(self.ztDataCount)
        print(self.dtDataCount)
        list = OrderedDict(sorted(tick.items(), key=lambda i: i[1]['amount'], reverse=1))
        # 通用事件
        event1 = Event(type_=EVENT_TICK)
        event1.dict_['data'] = list
        self.eventEngine.put(event1)

    def stockFilter(self,str):
        strRe = re.search("s[hz][036][0]",str)
        if(strRe != None):
            return True
        else:
            return False

    def setPlanList(self,str,list=[]):
        res = self.isContainOfList(str,list)
        return res

    def isContainOfList(self,str,list=[]):
        if str in list:
            return True
        else:
            return False

    def ztCount(self,close,now):
        zt = round(close*1.1,2)
        if(zt == now):
            return True
        else:
            return False

    def dtCount(self,close,now):
        dt = round(close*0.9,2)
        if(dt == now):
            return True
        else:
            return False
