from PyQt5.QtCore import *

from .eventEngine import *
import easyquotation
from .vtEvent import *
from collections import OrderedDict
from moniterEngine.saveData import *
import re
import time

class MarketDataThread(QThread):
    def __init__(self, eventEngine):
        super(MarketDataThread, self).__init__()
        """Constructor"""
        self.eventEngine = eventEngine
        print("MarketDataThread")
        # 事件引擎开关
        self.__active = True
        self.ztDataCount =0
        self.marketInfo = {'mainboard':'0','secondboard':'0','limitupRatio':'0%','rise':'0','fall':'0','--':'0','limitup':'0','limitdown':'0','boom':'0'}

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
        print(time.time())
        tick = self.quotation.market_snapshot(prefix=True)
        self.onTick(tick)


    def getMarketInfo(self):
        info = self.quotation.stocks(['sh000001','sz399006'], prefix=True)
        res = format((info['sh000001']['now']-info['sh000001']['close']) / info['sh000001']['close'], ".2%")
        # print("上证：%s"%(res))
        self.marketInfo["mainboard"] = res
        res = format((info['sz399006']['now']-info['sz399006']['close']) / info['sz399006']['close'], ".2%")
        # print("创业板：%s"%(res))
        self.marketInfo["secondboard"] = res
        event1 = Event(type_=EVENT_MARKETINFO)
        event1.dict_['data'] = self.marketInfo
        self.eventEngine.put(event1)

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
        # print(len(tick))
        custList1 = storeRecord("cust1")
        list = custList1.dataLoad()
        if(list == None):
            list=[]
        PlanAList = list[0]
        PlanCustList = ["300251", "600222", "300333"]
        self.ztDataCount =0
        self.ztBoomDataCount =0
        self.dtDataCount =0
        self.fallDataCount = 0
        self.riseDataCount = 0
        self.pDataCount = 0
        for code in tick:
            close = self.dict_get(tick[code], 'close')
            now = self.dict_get(tick[code], 'now')
            high = self.dict_get(tick[code], 'high')
            if close != 0:
                zf = (now - close) / close
            else:
                zf = 0

            if(zf > 0 and self.stockFilter(code)):
                self.riseDataCount +=1
            elif(zf <0 and self.stockFilter(code)):
                self.fallDataCount +=1
            elif(zf ==0 and self.stockFilter(code)):
                self.pDataCount +=1
            tick[code]['amount'] = zf
            ret = self.ztCount(close, now)
            if (ret == True and zf>0.06):
                self.ztDataCount += 1
            ret = self.ztBoomCount(close, high, now)

            if(close != 0):
                notSt = (high-close)/close

                if (ret == True and notSt > 0.06 and self.stockFilter(code)):
                    self.ztBoomDataCount += 1

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


        # print("zhangting:")
        # # print("涨停家数："%(self.ztDataCount))
        # print("涨停家数： %d" % (self.ztDataCount))
        # print("跌停家数： %d" % (self.dtDataCount))
        # print("炸板家数： %d" % (self.ztBoomDataCount))
        # print("上涨家数：%d  下跌家数：%d 平盘家数：%d"%(self.riseDataCount,self.fallDataCount,self.pDataCount))

        res = format(self.ztDataCount/(self.ztDataCount+self.ztBoomDataCount), ".2%")
        # print("封板率： %s" % (res))
        # {'mainboard': '0', 'secondboard': '0', 'limitupRatio': '0%', 'rise': '0', 'fall': '0', '--': '0',
        #  'limitup': '0', 'limitdown': '0', 'boom': '0'}

        self.marketInfo['limitup'] = str(self.ztDataCount)
        self.marketInfo['limitdown'] = str(self.dtDataCount)
        self.marketInfo['boom'] = str(self.ztBoomDataCount)
        self.marketInfo['rise'] = str(self.riseDataCount)
        self.marketInfo['fall'] = str(self.fallDataCount)
        self.marketInfo['--'] = str(self.pDataCount)
        self.marketInfo['limitupRatio'] = res

        self.getMarketInfo()
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

    def ztBoomCount(self,close,high,now):
        zt = round(close*1.1,2)
        if(zt == high and now < high):
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
