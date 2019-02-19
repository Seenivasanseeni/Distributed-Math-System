import socket
import json
import utils
import threading

MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT_CLIENT = 9000
MASTER_TCP_PORT_SLAVE = 9001

SLAVE_TCP_PORT = 10001

def getSlaveAddress():
    return "127.0.0.1"
def getToken():
    return "Ai,mn42"

def connect_clients():
    print("Listening for Clients...")
    skt= socket.socket(type=socket.SOCK_STREAM)
    skt.bind((MASTER_ADDRESS,MASTER_TCP_PORT_CLIENT))
    skt.listen(10)
    while True:
        clientsocket,address = skt.accept()
        msg = utils.receiveMessageTCP(clientsocket)
        print("LOG: Got message",msg)
        slaveAddress = getSlaveAddress()
        token = getToken()
        response = {
            "slave":slaveAddress,
            "token":token
        }
        utils.sendMessageTCP(clientsocket,json.dumps(response))
    print("Service for Clients is closing")

def connect_slaves():
    print("Listening for Slaves")
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.bind((MASTER_ADDRESS, MASTER_TCP_PORT_SLAVE))
    skt.listen(10)
    while True:
        slavesocket,address = skt.accept()
        msg = utils.receiveMessageTCP(slavesocket)
        print("LOG: Got message", msg)
    print("Service for Slaves is closing")

clientThread = threading.Thread(target=connect_clients)
slaveThread = threading.Thread(target=connect_slaves)

clientThread.start()
slaveThread.start()
clientThread.join()
slaveThread.join()
