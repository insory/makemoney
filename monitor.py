# -*- coding: utf-8 -*-
import sys
import easyquotation
from PyQt5.QtGui import *
from skimage import io


from moniterEngine.marketmonitor import *
from moniterEngine.mainWindow import *
from moniterEngine.tickdata import *

QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf8"))




# 直接运行脚本可以进行测试
if __name__ == '__main__':
    app = QApplication(sys.argv)
    easyquotation.update_stock_codes();
    ee = EventEngine()
    myqq = mainWindow(ee)
    # myqq.setWindowFlags(myqq.windowFlags()& ~Qt.WindowMinMaxButtonsHint)
    # myqq.setWindowTitle("monitor")


    ss = MarketMonitor(ee)
    kk = MarketDataThread(ee)
    kk.start(True)
    ee.start(True)
    sleep(1)
    myqq.show()
    app.exec_()
