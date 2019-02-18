import json
import socket
from utils import *
from config_port_address import *


skt=0
operation = {} #empty operation
operation_str = ""
def makeOperation(op,**kwparams):
    '''

    :param op: operator like ADD, SUB. DIV
    :param kwparams: operands 12 34
    :return:
    '''
    global  operation,operation_str
    operation={
        'OP':op,
        **kwparams
    }
    operation_str=json.dumps(operation)
    return

makeOperation("ADD",op1=12,op2=34)

def OR():
    '''This func should send a OR request to server and get the results back
    op: operation name such as ADD,SUB
    kwparams: list of operands
    '''
    global skt,operation,operation_str

    #create a socket
    skt = socket.socket(type=socket.SOCK_DGRAM)

    try:
        #set a timeout
        skt.settimeout(10)

        #send the message to master
        skt.sendto(bytes(operation_str,encoding='UTF-8'),(MASTER_UDP_ADDRESS,MASTER_UDP_LISTEN_CLIENT_PORT))

    except socket.error as socketerror:
        print("Error connecting to master",socketerror)

    #close the connection
    skt.close()

    #reintialize a socket and listen on a port - we can use the above socket itself and bind it
    skt = socket.socket(type=socket.SOCK_DGRAM)
    skt.bind(('localhost',CLIENT_UDP_RECEIVE_PORT))

    #get the reply from master to receive address of slave
    message,master_ip_address = receiveMessage(skt)

    #close the connection
    skt.close()
    return message


def getSlaveAddress(response):
    '''

    :param response: a JSON response for a OR
    :return:
    '''
    return response["slave"]

reply_from_master = None
try:
    reply_from_master = OR()
    print(reply_from_master)
except socket.error as socketerror:
    print("Timeout Error from master. retry later")

response_from_master=json.loads(reply_from_master)

slave_ip = None

try:
    slave_ip=getSlaveAddress(response_from_master)

    #open a TCP connection to slave
    skt = socket.socket(type=socket.SOCK_STREAM)
    skt.connect((slave_ip,SLAVE_CLIENT_SERVER_PORT))
    result = receiveMessageTCP(skt)
    print("RESULT:",result)
    skt.close()

except socket.error as socketerror:
    print("Timeout Error with slave")
