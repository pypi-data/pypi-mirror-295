import time
import timeit
import datetime

from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal


class FuncThread(Thread):
    def __init__(self, target, *args):
        self._Func = target
        self._Param = args
        Thread.__init__(self)

    def run(self):
        self._Func(*self._Param)


class threadIndicate(QThread):
    updateDate = pyqtSignal(bool, str, str, str)
    updateIcon = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.main = parent
        self.isRun = False
        self.startTime = 0.0
        self.endTime = 0.0

    def run(self):
        self.endTime = self.startTime = timeit.default_timer()
        while self.isRun:
            self.setDateTime()
            self.setIndicateIcon()
            time.sleep(1)

    def stop(self):
        self.isRun = False

    def setIndicateIcon(self):
        self.updateIcon.emit()

    def setDateTime(self):
        now = datetime.datetime.now()  # 2099-09-09 09:09:09.999999
        nowDate = now.strftime('%Y-%b-%d')  # 2099-Sep-9
        nowDateKor = now.strftime('%Y-%m-%d')  # 2099-9-9
        nowTime = now.strftime('%H:%M:%S')  # 09:09:09
        self.updateDate.emit(True, nowDate, nowDateKor, nowTime)


class threadTimer(QThread):
    timerFinish = pyqtSignal(bool)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.isRun = False
        self.finishEvent = True
        self.startTime = 0.0
        self.endTime = 0.0
        self.outTime = 0.0

    def run(self):
        self.endTime = self.startTime = timeit.default_timer()
        while self.isRun:
            self.endTime = timeit.default_timer()
            self.duringTime = self.endTime - self.startTime
            if self.duringTime < self.outTime:
                time.sleep(0.148)
            elif self.during_time > self.outTime:
                self.isRun = False
                break

        if self.finishEvent:
            self.timerFinish.emit(True)

    def stop(self):
        self.isRun = False
        self.finishEvent = False


class threadWatchDog(QThread):
    procWorkChecking = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.isRun = False

    def run(self):
        while self.isRun:
            self.procWorkChecking.emit()
            time.sleep(0.999)

    def stop(self):
        self.isRun = False
