

from PyQt5.QtNetwork import QTcpSocket

s = QTcpSocket()
s.connectToHost('127.0.0.1', 5000)
s.readyRead.connect(lambda x: print(x))
s.error.connect(lambda x: print(x))

s.write('start\n'.encode())
s.waitForBytesWritten(1000)
s.waitForReadyRead()
s.readAll()
