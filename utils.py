import socket

def receiveMessage(skt):
    '''
    Get the bytes from socket and return it as a string
    :param skt: a binded UDP socket
    :return:
    '''
    skt.settimeout(20) # timeout for receiving first packet
    message=""
    ip_address=None
    try:
        while True:
            msg,add=skt.recvfrom(1024)
            ip_address=add
            message = message + msg.decode('UTF-8')
            skt.settimeout(10)
    except socket.error as socketerror:
        print("LOG: Message Received",message,"from",ip_address)
    try:
        return message,ip_address[0]
    except:
        raise Exception("No single UDP packet is received")

def sendMessage(skt,message,address_tuple):
    '''
    :param skt: socket
    :param message: message in string
    :param address: address of the machine(master/slave/client)in the format (ip,port)
    :return:
    '''
    skt.sendto(bytes(message,encoding='UTF-8'),address_tuple)
    return

def receiveMessageTCP(skt):
    '''

    :param skt: a connected TCP socket
    :return:
    '''
    message= skt.recv(1024).decode('UTF-8') #todo find a way if there are many packets in stream
    return message
