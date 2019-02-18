BUFF_SIZE = 1024
def sendMessageTCP(skt,message):
    '''
    send a message through TCP
    :param skt: a connected or binded socket socket
    :param message: a string that needs to be send
    :return:
    '''
    skt.send(bytes(message,encoding='UTF-8'))
    return

def receiveMessageTCP(skt):
    '''
    receive the message through TCP
    :param skt: a connected or binded socket socket
    :return: message received from the other end
    '''
    messageBytes = skt.recv(BUFF_SIZE)
    return messageBytes.decode('UTF-8')
