
from  qtpy import QtWidgets,QtCore
from  PyQt5.QtWidgets import QTableWidgetItem
from .vtEvent import *
from collections import OrderedDict
from .eventEngine import  *
from PyQt5.Qt import *
class BasicMonitor(QtWidgets.QTableWidget):
    """
    基础监控

    headerDict中的值对应的字典格式如下
    {'chinese': u'中文名', 'cellType': BasicCell}

    """
    signal = QtCore.Signal(type(Event()))

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine=None, eventEngine=None, parent=None):
        """Constructor"""
        super(BasicMonitor, self).__init__(parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # 保存表头标签用
        self.headerDict = OrderedDict()  # 有序字典，key是英文名，value是对应的配置字典
        self.headerList = []  # 对应self.headerDict.keys()

        # 保存相关数据用
        self.dataDict = {}  # 字典，key是字段对应的数据，value是保存相关单元格的字典
        self.dataKey = ''  # 字典键对应的数据字段

        # 监控的事件类型
        self.eventType = ''

        # 列宽调整状态（只在第一次更新数据时调整一次列宽）
        self.columnResized = False

        # 字体
        self.font = None

        # 保存数据对象到单元格
        self.saveData = False

        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = True

    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        #col = len(self.headerDict)
        #self.setColumnCount(col)
        self.setColumnCount(5)

        # 设置列表头
        labels = ["公司","价格", "涨幅", "代码", "未定义"]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)

        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设为行交替颜色
        self.setAlternatingRowColors(True)

        # 设置允许排序
        self.setSortingEnabled(self.sorting)

        self.setRowCount(4728)

        self.horizontalHeader().setStretchLastSection(True)


        self.setColumnWidth(0,60)
        self.setColumnWidth(1,50)
        self.setColumnWidth(2,60)
        self.setColumnWidth(3,70)

        for index in range(self.columnCount()):
            headItem = self.horizontalHeaderItem(index)
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)


class MarketMonitor(BasicMonitor):
    """市场监控组件"""

    # ----------------------------------------------------------------------
    def __init__(self, eventEngine, parent=None):
        """Constructor"""
        super().__init__(self, eventEngine, parent=None)

        # 设置监控事件类型
        self.setEventType(EVENT_TICK)

        # 注册事件监听
        self.registerEvent()

        self.initTable()


    # ----------------------------------------------------------------------
    def setEventType(self, eventType):
        """设置监控的事件类型"""
        self.eventType = eventType

    def registerEvent(self):
        """注册GUI更新相关的事件监听"""
        self.signal.connect(self.updateEvent)
        self.eventEngine.register(self.eventType, self.signal.emit)


    # ----------------------------------------------------------------------
    def updateEvent(self, event):
        """收到事件更新"""
        data = event.dict_['data']
        self.updateData(data)

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
    # ----------------------------------------------------------------------
    def updateData(self, data):
        """将数据更新到表格中"""
        StockValues = OrderedDict()
        i = 0
        for code in data:
            open = self.dict_get(data[code],'close')
            now = self.dict_get(data[code],'now')
            if open != 0:
                zf = (now-open)/open
            else:
                zf = 0
            data[code]['amount'] = zf
            i = i + 1
        list = OrderedDict(sorted(data.items(), key=lambda i: i[1]['amount'],reverse=1))
        j = 0
        for show in list:
            self.setItem(j, 0, QTableWidgetItem(list[show]['name']))
            self.setItem(j, 1, QTableWidgetItem(str(list[show]['now'])))
            res = format(list[show]['amount'],".2%")
            self.setItem(j, 2, QTableWidgetItem(str(res)))
            self.setItem(j, 3, QTableWidgetItem(show))
            j=j+1



