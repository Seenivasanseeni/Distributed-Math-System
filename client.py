import json
import socket
from utils import *
from config_port_address import *




def OR(op,**kwparams):
    '''This func should send a OR request to server and get the results back
    op: operation name such as ADD,SUB
    kwparams: list of operands
    '''
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
    print(message)
    return
OR('ADD',k=2,t=4)
