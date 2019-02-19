import json
import socket
import utils
import threading

MASTER_ADDRESS = '192.168.167.213'
MASTER_TCP_PORT_CONNECT_SLAVE = 9001

SLAVE_TCP_PORT = 9001


class SlaveClientThread(threading.Thread):
    def __init__(self,message):
        threading.Thread.__init__(self)
        print("Trying to connect to master....")
        self.skt = socket.socket(type=socket.SOCK_STREAM) #tcp connection
        self.connect((MASTER_TCP_PORT_CONNECT_SLAVE,MASTER_ADDRESS))
        print("Connection to the Master Established...")

    def run(self):
        '''
        Listen for connections and then run
        :return:
        '''




def connect_to_master():
    '''
        connect the slave to the master
    :return: a connected socket
    '''
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.connect((MASTER_ADDRESS,MASTER_TCP_PORT_CONNECT_SLAVE))
    connect = {
        "action":"connect",
    }
    connect_message = json.dumps(connect,MASTER_TCP_PORT_CONNECT_SLAVE)
    utils.sendMessageTCP(skt,connect_message)
    return skt

def slave_thread():
    print("Trying to connect to master")
    skt = connect_to_master()
    print("Connection Successful")

    print("Listening for message from master")
    while True:
        message_str = utils.receiveMessageTCP(skt)
        print("LOG: Got message",message_str)
        message = json.loads(message_str)
        newClient= SlaveClientThread(message)
        newClient.start()

driverThread = threading.Thread(target=slave_thread)
driverThread.start()
driverThread.join()
