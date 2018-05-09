# -*- coding: utf-8 -*-
import sys
import easyquotation
from PyQt5.QtGui import *
from skimage import io


from moniterEngine.marketmonitor import *
from moniterEngine.stocksearch import *
from moniterEngine.tickdata import *

QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf8"))


class MyQQ(QTabWidget):
    def __init__(self,eventEngine, parent=None):
        super(MyQQ, self).__init__(parent)
        palette1 = QPalette()
        self.frame = 1
        self.setPalette(palette1)

        tab1 = MarketMonitor(eventEngine)

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
        stocksearch1 = stocksearch()
        vlayout3 = QVBoxLayout(groupbox3)
        vlayout3.setAlignment(Qt.AlignCenter)
        vlayout3.addWidget(stocksearch1)
        vlayout3.addWidget(tab3)

        toolbox1 = QToolBox()
        toolbox1.setPalette(palette1)
        toolbox1.setAutoFillBackground(True)

        toolbox1.addItem(groupbox1, self.tr("list 1"))
        toolbox1.addItem(groupbox2, self.tr("list A"))
        toolbox1.addItem(groupbox3, self.tr("list B"))

        # search=stocksearch()
        testbutton = QPushButton()
        toolbox2 = QToolBox()
        toolbox2.addItem(testbutton,"get")
        # toolbox2.addItem(search,"111")
        toolbox2.setPalette(palette1)
        toolbox2.setAutoFillBackground(True)
        testbutton.clicked.connect(lambda:self.buttonTest())

        self.addTab(toolbox1, "主面板")
        self.addTab(toolbox2, "监控")
        self.setAutoFillBackground(True)

        toolbox1.setStyleSheet("background:rgb(60,60,60);border:0px solid rgb(80, 80, 80);border-radius: 10px")
        toolbox2.setStyleSheet("background:rgb(60,60,60);border:0px solid rgb(0, 225, 230)")

        tab1.setStyleSheet("background:rgb(60,60,60);border:0px solid rgb(0, 225, 230)")
        tab2.setStyleSheet("background:rgb(60,60,60);border:0px solid rgb(0, 225, 230)")

        self.setGeometry(300, 300, 200, 500)
        # self.setGeometry(300, 300, 200, 500)


    def buttonTest(self):
        image = io.imread("http://image.sinajs.cn/newchart/daily/n/sh601006.gif")
        io.imshow(image)
        io.show()

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

        self.show()

# 直接运行脚本可以进行测试
if __name__ == '__main__':
    app = QApplication(sys.argv)
    easyquotation.update_stock_codes();
    ee = EventEngine()
    myqq = MyQQ(ee)
    # myqq.setWindowFlags(myqq.windowFlags()& ~Qt.WindowMinMaxButtonsHint)
    # myqq.setWindowTitle("monitor")


    ss = MarketMonitor(ee)
    kk = MarketDataThread(ee)
    kk.start(True)
    ee.start(True)
    sleep(1)
    myqq.show()
    app.exec_()
