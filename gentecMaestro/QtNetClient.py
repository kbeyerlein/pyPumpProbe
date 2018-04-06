import sys
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from PyQt5 import QtNetwork


class MyApp(QWidget):
    threadSignal = pyqtSignal(object)
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 280, 600)
        self.setWindowTitle('using threads')

        self.layout = QVBoxLayout(self)

        self.startBtn = QPushButton("Start")
        self.startBtn.released.connect(self.startAq)
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.released.connect(self.stopAq)
        self.listwidget = QListWidget(self)

        self.layout.addWidget(self.startBtn)
        self.layout.addWidget(self.stopBtn)
        self.layout.addWidget(self.listwidget)

        self.threadPool = []
        self.measure = True

        self.threadSignal.connect(self.add)

        # Network stuff
        self.tcpClient = QtNetwork.QTcpSocket()
        self.tcpClient.connectToHost('127.0.0.1', 5000)
        self.tcpClient.readyRead.connect(self.getData)
        self.tcpClient.error.connect(lambda x: print(x))

    def add(self, text):
        """ Add item to list widget """
        self.listwidget.addItem(text)
        self.listwidget.sortItems()

    def getData(self, delay=0.3):
        '''
        """ Add several items to list widget """
        while self.measure:
            self.threadSignal.emit('hallo')
            time.sleep(delay)  # artificial time delay
        '''
        self.add(self.tcpClient.readLine(1024).decode().rstrip())

    def startAq(self):
        self.tcpClient.write('start\n'.encode())
        '''
        my_thread = QThread() # create the QThread
        my_thread.start()
        self.measure = True

        # This causes my_worker.run() to eventually execute in my_thread:
        my_worker = GenericWorker(self.getData)
        my_worker.moveToThread(my_thread)
        my_worker.start.emit("hello")
        # my_worker.finished.connect(self.xxx)

        self.threadPool.append(my_thread)
        self.my_worker = my_worker
        '''

    def stopAq(self):
        self.measure = False
        self.tcpClient.write('stop\n'.encode())

    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())
  


class GenericWorker(QObject):
    start = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    @pyqtSlot(str)
    def run(self, *args, **kwargs):
        self.function(*self.args, **self.kwargs)
        self.finished.emit()

if __name__ == '__main__':
    # run
    app = QApplication(sys.argv)
    test = MyApp()
    test.show()
    app.exec_()

