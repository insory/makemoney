
from  qtpy import QtWidgets,QtCore
from PyQt5 import QtGui
from  PyQt5.QtWidgets import QTableWidgetItem
from .vtEvent import *
from collections import OrderedDict
from .eventEngine import  *
from PyQt5.Qt import *
from  moniterEngine.searchcode import *
from moniterEngine.saveData import *

class BasicMonitor(QTableWidget):
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
        self.mouseStatus = False

        # 保存数据对象到单元格
        self.saveData = False

        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = False

        self.daylinewidget = None
        self.search = searchcode()
        self.stockItemText = None

        # 设置悬停显示
        self.setMouseTracking(True)
        self.itemEntered.connect(self.handleItemClicked)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        print("press")
        code = self.search.findbychinese(self.stockItemText)
        if(len(code) == 0):
            return
        print(code[0])
        self.mouseStatus = True
        if (e.button() == Qt.LeftButton):
            self.daylineshow(code[0], "left")
        elif (e.button() == Qt.RightButton):
            self.daylineshow(code[0], "right")
        elif(e.button() == Qt.MidButton):
            self.mouseStatus = False


    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        print("release")
        self.daylinehide()
        self.mouseStatus = False

    def handleItemClicked(self, item):
        self.stockItemText = item.text()
        print(item.text())


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

    def daylineinit(self):
        url = 'http://image.sinajs.cn/newchart/min/n/sh000001.gif'
        req = requests.get(url)

        photo = QPixmap()
        photo.loadFromData(req.content)

        label = QLabel()
        label.setPixmap(photo)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(label)

        return widget



    def daylineshow(self,code,str):
        if(code[0] == '6'):
            if(str == "left"):
                url = 'http://image.sinajs.cn/newchart/min/n/sh'+code+'.gif'
            elif(str == "right"):
                url = 'http://image.sinajs.cn/newchart/daily/n/sh' + code + '.gif'
        else:
            if (str == "left"):
                url = 'http://image.sinajs.cn/newchart/min/n/sz' + code + '.gif'
            elif (str == "right"):
                url = 'http://image.sinajs.cn/newchart/daily/n/sz' + code + '.gif'
        # url = url.match("sh000001","300279")
        print(url)
        req = requests.get(url)

        photo = QPixmap()
        photo.loadFromData(req.content)
        label = QLabel()

        label.setPixmap(photo)
        label.setWindowOpacity(0.2)

        self.daylinewidget = QWidget()

        self.daylinewidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background,QColor(128, 128, 128, 50))
        self.daylinewidget.setPalette(palette)
        self.daylinewidget.resize( 50 , 50 );
        label.setPalette(palette)
        layout = QVBoxLayout()
        self.daylinewidget.setLayout(layout)
        layout.addWidget(label)
        self.daylinewidget.setGeometry(500,300,50,50)
        self.daylinewidget.show()

    def daylinehide(self):
        if(self.mouseStatus == True):
            self.daylinewidget.hide()

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
        # self.setAlternatingRowColors(True)

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


    # ----------------------------------------------------------------------
    def updateData(self, data):
        """将数据更新到表格中"""
        j = 0
        for show in data:
            if(data[show]["valid"] == True and data[show]["amount"]>-0.2):
                self.setItem(j, 0, QTableWidgetItem(data[show]['name']))
                self.setItem(j, 1, QTableWidgetItem(str(data[show]['now'])))
                res = format(data[show]['amount'],".2%")
                self.setItem(j, 2, QTableWidgetItem(str(res)))
                self.setItem(j, 3, QTableWidgetItem(show))
                self.setItem(j, 4, QTableWidgetItem(str(j)))
                j=j+1

class CustomMonitor(BasicMonitor):
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

    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        self.setColumnCount(5)

        # 设置列表头
        labels = ["公司","价格", "涨幅", "代码", "自定义"]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)

        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设为行交替颜色
        # self.setAlternatingRowColors(True)

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

    def updateData(self, data):
        j = 0
        for show in data:
            if (data[show]["planCust"] == True):
                self.setItem(j, 0, QTableWidgetItem(data[show]['name']))
                self.setItem(j, 1, QTableWidgetItem(str(data[show]['now'])))
                res = format(data[show]['amount'], ".2%")
                self.setItem(j, 2, QTableWidgetItem(str(res)))
                self.setItem(j, 3, QTableWidgetItem(show))
                j = j + 1


class PlanAMonitor(BasicMonitor):
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

        self.itemDoubleClicked.connect(self.delstock)

        self.search = searchcode()
        self.custList1 = storeRecord("cust1")

    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        self.setColumnCount(5)

        # 设置列表头
        labels = ["公司","价格", "涨幅", "代码", "自定义"]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)

        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设为行交替颜色
        # self.setAlternatingRowColors(True)

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

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        super().mousePressEvent(e)
        if(e.button() == Qt.MidButton):
            self.delstock(self.stockItemText)

    def delstock(self,str):
        print(str)
        code = self.search.findbychinese(str)
        print(code[0])
        self.custList1.dataDel(code[0])
        self.removeRow(self.currentRow())

    def updateData(self, data):
        j = 0
        self.clear()
        labels = ["公司", "价格", "涨幅", "代码", "自定义"]
        self.setHorizontalHeaderLabels(labels)
        for show in data:
            if (data[show]["planA"] == True ):
                self.setItem(j, 0, QTableWidgetItem(data[show]['name']))
                self.setItem(j, 1, QTableWidgetItem(str(data[show]['now'])))
                res = format(data[show]['amount'], ".2%")
                self.setItem(j, 2, QTableWidgetItem(str(res)))
                self.setItem(j, 3, QTableWidgetItem(show))
                self.setItem(j, 4, QTableWidgetItem(str(j)))
                j = j + 1