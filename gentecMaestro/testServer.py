# http://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
import socket
import threading
import numpy as np
import time

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('listening on: ', host, port)
        self.measure = False

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print(client, address, 'connected')
            #client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                    args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                print(data)
                if data == 'start\n'.encode():
                    self.measure = True
                    threading.Thread(target = self.sendData, args = (client,address)).start()
                elif data == 'stop\n'.encode():
                    self.measure = False
                elif data:
                    # Set the response to echo back the recieved data 
                    response = data.upper()
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def sendData(self, client, address):
        while self.measure:
            client.send((str(np.random.rand())+'\n').encode())
            time.sleep(0.1)
        

if __name__ == "__main__":
    #port_num = input("Port? ")
    port_num = 5000
    ThreadedServer('',port_num).listen()
