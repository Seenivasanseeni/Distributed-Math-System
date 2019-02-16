import socket
import json
from utils import  *
from config_port_address import *

#open socket
skt=socket.socket(type=socket.SOCK_DGRAM)

#bind the port
skt.bind(('localhost',MASTER_UDP_LISTEN_CLIENT_PORT))

while True:
    #receive the message
    operation_msg,client_ip_address = receiveMessage(skt)
    operation = json.loads(operation_msg)
    print(operation)
    sendMessage(skt,operation_msg,(client_ip_address,CLIENT_UDP_RECEIVE_PORT))

    #spawn a separate thread using operation as an argument
