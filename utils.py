def receiveMessage(skt):
    '''
    Get the bytes from socket and return it as a string
    :param skt: a binded UDP socket
    :return:
    '''
    skt.settimeout(10) # timeout for receiving
    message=""
    ip_address=None
    try:
        msg,add=skt.recvfrom(1024)
        ip_address=add
        message = message + msg.decode('UTF-8')
    except TimeoutError:
        pass
    return message,ip_address[0]

def sendMessage(skt,message,address_tuple):
    '''

    :param skt: socket
    :param message: message in string
    :param address: address of the machine(master/slave/client)in the format (ip,port)
    :return:
    '''
    skt.sendto(bytes(message,encoding='UTF-8'),address_tuple)
    return
