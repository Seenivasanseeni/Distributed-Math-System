import socket
import json
import utils
import threading
import random

MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT_CLIENT = 9000
MASTER_TCP_PORT_SLAVE = 9001


def getSlaveAddress():
    '''
    To get a address of a slave to which message needs to be send
    :return:
    '''
    global slaves
    if(len(slaves)==0):
        return "127.0.0.1" #todo handle special case
    return slaves[random.randrange(0,len(slaves))]

def getToken():
    return "Ai,mn42"

slaves =[]
def connect_clients():
    print("Listening for Clients on port {}...".format(MASTER_TCP_PORT_CLIENT))
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
    global  slaves
    print("Listening for Slaves on port {}...".format(MASTER_TCP_PORT_SLAVE))
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.bind((MASTER_ADDRESS, MASTER_TCP_PORT_SLAVE))
    skt.listen(10)
    while True:
        slavesocket,(address,port) = skt.accept()
        msg_str = utils.receiveMessageTCP(slavesocket)
        print("LOG: Got message", msg_str)
        msg = json.loads((msg_str))
        action = msg["action"]
        if action == "connect":
            print("Connection request from Slave at {} ....".format(address))
            slaves.append(address) #todo needs to be handled for mutual exclusion
            print("Slave Added...")
    print("Service for Slaves is closing")

clientThread = threading.Thread(target=connect_clients)
slaveThread = threading.Thread(target=connect_slaves)

clientThread.start()
slaveThread.start()
clientThread.join()
slaveThread.join()
