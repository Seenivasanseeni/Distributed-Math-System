import json
import socket
import utils
import threading

MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT_CONNECT_SLAVE = 9001

SLAVE_TCP_PORT_CLIENT = 10001
skt_master = None
skt_client_server = None

class SlaveClientThread(threading.Thread):

    def __init__(self,message):
        '''

        :param message: a JSON object from master regarding connection to client
        '''
        threading.Thread.__init__(self)
        print("Initiating a new Thread for a client with message",message)
        self.token = message["token"]

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
    print("Trying to connect to master")
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.connect((MASTER_ADDRESS,MASTER_TCP_PORT_CONNECT_SLAVE))
    connect = {
        "action":"connect",
    }
    connect_message = json.dumps(connect)
    utils.sendMessageTCP(skt,connect_message)
    print("Connection to Master Successful")
    return skt

def slave_thread():
    skt = connect_to_master()
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
