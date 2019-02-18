import socket
import json
from utils import  *
from config_port_address import *

#open socket
skt_listen=socket.socket(type=socket.SOCK_DGRAM)
skt_send = socket.socket(type=socket.SOCK_DGRAM)

#bind the port
skt_listen.bind(('localhost',MASTER_UDP_LISTEN_CLIENT_PORT))

while True:
    #receive the message
    operation_msg,client_ip_address = receiveMessage(skt_listen)
    operation = json.loads(operation_msg)
    print(operation)
    response = {
        'slave' : '127.0.0.1'
    }
    sendMessage(skt_send,json.dumps(response),(client_ip_address,CLIENT_UDP_RECEIVE_PORT))

    #spawn a separate thread using operation as an argument
