# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.Qt import *
from qtpy import *


from moniterEngine.marketmonitor import *
from moniterEngine.tickdata import *
import sys

QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf8"))


class MyQQ(QTabWidget):
    def __init__(self,eventEngine, parent=None):
        super(MyQQ, self).__init__(parent)

        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(128, 128, 128))  # 设置背景颜色
         # palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('../../../Document/images/17_big.jpg')))   # 设置背景图片
        self.frame = 1
        self.setPalette(palette1)
        tab1 = MarketMonitor(eventEngine)
        tab1.setPalette(palette1)
        groupbox1 = QGroupBox()
        groupbox1.setPalette(palette1)
        vlayout1 = QVBoxLayout(groupbox1)
        vlayout1.setAlignment(Qt.AlignCenter)
        vlayout1.addWidget(tab1)

        tab2 = CustomMonitor(eventEngine)
        tab2.setPalette(palette1)
        groupbox2 = QGroupBox()
        groupbox2.setPalette(palette1)
        vlayout2 = QVBoxLayout(groupbox2)
        vlayout2.setAlignment(Qt.AlignCenter)
        vlayout2.addWidget(tab2)

        tab3 = PlanAMonitor(eventEngine)
        tab3.setPalette(palette1)
        groupbox3 = QGroupBox()
        groupbox3.setPalette(palette1)
        vlayout3 = QVBoxLayout(groupbox3)
        vlayout3.setAlignment(Qt.AlignCenter)
        vlayout3.addWidget(tab3)

        toolbox1 = QToolBox()
        toolbox1.setPalette(palette1)
        toolbox1.setAutoFillBackground(True)
        toolbox1.addItem(groupbox1, self.tr("我的自选"))
        toolbox1.addItem(groupbox2, self.tr("近期强势股"))
        toolbox1.addItem(groupbox3, self.tr("我的交易计划"))

        toolbox2 = QToolBox()
        toolbox2.setPalette(palette1)
        toolbox2.setAutoFillBackground(True)
        self.addTab(toolbox1, "主面板")
        self.addTab(toolbox2, "监控")
        self.setAutoFillBackground(True)
    def buttonClicked(self,toolbox1):
        groupboxNew = QGroupBox()
        toolboxNew = QToolBox()
        toolbox1.addItem(groupboxNew,self.tr("new group"))
    def enterEvent(self, evt):
        self.activateWindow()
        if(self.x() == self.frame-self.width()):
            self.move(-self.frame,self.y())
        elif(self.y() == self.frame-self.height()+self.y()-self.geometry().y()):
            self.move(self.x(),-self.frame)
    def leaveEvent(self,evt):
        cx,cy=QCursor.pos().x(),QCursor.pos().y()
        if(cx >= self.x() and cx <= self.x()+self.width()
            and cy >= self.y() and cy <= self.geometry().y()):
            return#title bar
        elif(self.x() < 0 and QCursor.pos().x()>0):
            self.move(self.frame-self.width(),self.y())
        elif(self.y() < 0 and QCursor.pos().y()>0):
            self.move(self.x(), self.frame-self.height()+self.y()-self.geometry().y())

# 直接运行脚本可以进行测试
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ee = EventEngine()
    myqq = MyQQ(ee)
    myqq.setWindowFlags(myqq.windowFlags()& ~Qt.WindowMinMaxButtonsHint)
    myqq.setWindowTitle("自动量化交易")

    ss = MarketMonitor(ee)
    kk = MarketDataThread(ee)
    kk.start(True)
    ee.start(True)
    sleep(1)
    myqq.show()
    app.exec_()
