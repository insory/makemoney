# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.Qt import *


from moniterEngine.marketmonitor import *
from moniterEngine.tickdata import *
import sys

QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf8"))


class MyQQ(QTabWidget):
    def __init__(self,eventEngine, parent=None):
        super(MyQQ, self).__init__(parent)


        tab1 = MarketMonitor(eventEngine)
        #tab1.setColumnCount(3)
        #tab1.horizontalHeader().setDefaultSectionSize(50)
        #tab1.horizontalHeader().setStretchLastSection(True)
        #tab1.setHorizontalHeaderLabels(header)

        toolButton2 = QToolButton()
        toolButton2.setText(self.tr("条件设置"))
        toolButton2.setIcon(QIcon("d:/image/2.png"))
        toolButton2.setIconSize(QSize(60, 60))
        toolButton2.setAutoRaise(True)
        toolButton2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        toolButton3 = QToolButton()
        toolButton3.setText(self.tr("为什么"))
        toolButton3.setIcon(QIcon("d:/image/3.png"))
        toolButton3.setIconSize(QSize(60, 60))
        toolButton3.setAutoRaise(True)
        toolButton3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        groupbox1 = QGroupBox()
        vlayout1 = QVBoxLayout(groupbox1)
        vlayout1.setAlignment(Qt.AlignCenter)
        vlayout1.addWidget(tab1)
        vlayout1.addWidget(toolButton2)
        vlayout1.addStretch()

        groupbox2 = QGroupBox()
        vlayout2 = QVBoxLayout(groupbox2)
        vlayout2.setAlignment(Qt.AlignCenter)
        vlayout2.addWidget(toolButton3)
        vlayout2.addStretch()

        groupbox3 = QGroupBox()

        toolbox1 = QToolBox()
        toolbox1.addItem(groupbox1, self.tr("自"))
        toolbox1.addItem(groupbox2, self.tr("头"))
        toolbox1.addItem(groupbox3, self.tr("今日"))

        toolbox2 = QToolBox()
        self.addTab(toolbox1, "选")
        self.addTab(toolbox2, "监控")
        list = QListWidgetItem

    def buttonClicked(self,toolbox1):
        groupboxNew = QGroupBox()
        toolboxNew = QToolBox()
        toolbox1.addItem(groupboxNew,self.tr("new group"))

# 直接运行脚本可以进行测试
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ee = EventEngine()
    myqq = MyQQ(ee)
    myqq.setWindowFlags(myqq.windowFlags()& ~Qt.WindowMinMaxButtonsHint)
    myqq.setWindowTitle("自动")

    ss = MarketMonitor(ee)
    kk = MarketDataThread(ee)
    kk.start(True)
    ee.start(True)
    sleep(1)
    myqq.show()
    app.exec_()
