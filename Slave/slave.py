import json
import socket
import utils
import threading


MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT_CLIENT = 9000
MASTER_TCP_PORT_SLAVE = 9001

SLAVE_TCP_PORT_CLIENT = 8000

skt_master = None

class SlaveClientThread(threading.Thread):

    def __init__(self,message):
        '''

        :param message: a JSON object from master regarding connection to client
        '''
        global skt_slave

        threading.Thread.__init__(self)
        print("Initiating a new Thread for a client with message",message)
        self.token = message["token"]
        print("Listening for clients in slave at port {}".format(SLAVE_TCP_PORT_CLIENT))
        self.skt = skt_slave

    def run(self):
        '''
        Listen for connections and then run
        :return:
        '''
        print("Listening for message from client at port {}...".format(SLAVE_TCP_PORT_CLIENT))
        client_socket,(address,port) = self.skt.accept()
        print("Connection establsihed from client",address,port)
        message_client_str = utils.receiveMessageTCP(client_socket)
        message_client = json.loads(message_client_str)
        print("Received Message:{}".format(message_client_str))
        op = message_client["OP"]
        response ={
            "result": message_client["op1"] +message_client["op2"]
        }
        response_str = json.dumps(response)
        utils.sendMessageTCP(client_socket,response_str)
        return

def connect_to_master():
    '''
        connect the slave to the master
    :return: a connected socket
    '''
    print("Trying to connect to master at {}:{}".format(MASTER_ADDRESS,MASTER_TCP_PORT_SLAVE))
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.connect((MASTER_ADDRESS,MASTER_TCP_PORT_SLAVE))
    connect = {
        "action":"connect",
    }
    connect_message = json.dumps(connect)
    utils.sendMessageTCP(skt,connect_message)
    print("Connection to Master Successful")
    return skt

def slave_thread():
    '''
    This thread is to serve users which is initiated by master
    :return:
    '''
    global skt_slave
    skt = connect_to_master()
    print("Listening for message from master")
    skt_slave = socket.socket(type=socket.SOCK_STREAM)
    skt_slave.bind(("127.0.0.1", SLAVE_TCP_PORT_CLIENT))
    skt_slave.listen(100)

    while True:
        message_str = utils.receiveMessageTCP(skt)
        print("LOG: Got message",message_str)
        message = json.loads(message_str)
        newClient= SlaveClientThread(message)
        newClient.start()

driverThread = threading.Thread(target=slave_thread)
driverThread.start()
driverThread.join()
