from PyQt5.QtCore import *

from .eventEngine import *
import easyquotation
from .vtEvent import *
class MarketDataThread(QThread):
    def __init__(self, eventEngine):
        super(MarketDataThread, self).__init__()
        """Constructor"""
        self.eventEngine = eventEngine
        print("MarketDataThread")
        # 事件引擎开关
        self.__active = True

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

    def onTick(self, tick):
        """市场行情推送"""
        print(len(tick))
        # 通用事件
        event1 = Event(type_=EVENT_TICK)
        event1.dict_['data'] = tick
        self.eventEngine.put(event1)