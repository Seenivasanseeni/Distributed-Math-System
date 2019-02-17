import json
import socket
from utils import *
from config_port_address import *


skt=0

def OR(op,**kwparams):
    '''This func should send a OR request to server and get the results back
    op: operation name such as ADD,SUB
    kwparams: list of operands
    '''
    global skt
    operation={
        'OP':op,
        **kwparams
    }
    operation_str=json.dumps(operation)

    #create a socket
    skt = socket.socket(type=socket.SOCK_DGRAM)

    #set a timeout
    skt.settimeout(10)

    #send the message to master
    skt.sendto(bytes(operation_str,encoding='UTF-8'),(MASTER_UDP_ADDRESS,MASTER_UDP_LISTEN_CLIENT_PORT))

    #reintialize a socket and listen on a port - we can use the above socket itself and bind it
    skt = socket.socket(type=socket.SOCK_DGRAM)
    skt.bind(('localhost',CLIENT_UDP_RECEIVE_PORT))

    #get the reply from master to receive address of slave
    message,master_ip_address = receiveMessage(skt)
    return message


def getSlaveAddress(response):
    '''

    :param response: a JSON response for a OR
    :return:
    '''
    return response["slave"]

reply_from_master = None
try:
    reply_from_master = OR('ADD',k=2,t=4)
    print(reply_from_master)
except socket.error as socketerror:
    print("Timeout Error from master. retry later")

response_from_master=json.loads(reply_from_master)

slave_ip = None
try:
    slave_ip=getSlaveAddress(response_from_master)
    #get the message from slave
    response_ip = None
    result=None
    while response_ip != slave_ip: #check whethere the response is from the slave or imposter
        msg,response_ip = receiveMessage(skt)
except socket.error as socketerror:
    print("Timreout Error with slave")
