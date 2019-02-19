import json
import socket
import utils


MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT_CLIENT = 9000
MASTER_TCP_PORT_SLAVE = 9001

SLAVE_TCP_PORT_CLIENT = 8000


#send a operation to master

operation = {
    "op": "ADD",
}

def make_operation(op,**kwparams):
    '''

    :param op: operation such as ADD,SUB..
    :param kwparams: operands for the operation
    :return:
    '''
    return {
        'OP':op,
        **kwparams
    }


operation_str = json.dumps({})
print("Connecting to Master {}:{}...".format(MASTER_ADDRESS,MASTER_TCP_PORT_CLIENT))
skt = socket.socket(type=socket.SOCK_STREAM)

skt.connect((MASTER_ADDRESS,MASTER_TCP_PORT_CLIENT))
print("Connection to Master successful...")

print("Sending message..",operation_str)
utils.sendMessageTCP(skt,operation_str)
print("Message sending done")

response_from_master_str = utils.receiveMessageTCP(skt)

response_from_master = json.loads(response_from_master_str)
print("Response from master: ",response_from_master)
skt.close()

token = response_from_master["token"]
slave_address = response_from_master["slave"]

print("Exp Failure: Trying to connect to slave {}:{}".format(slave_address,SLAVE_TCP_PORT_CLIENT))

#open a new socket and make a connection to slave
skt = socket.socket(type=socket.SOCK_STREAM)
skt.connect((slave_address,SLAVE_TCP_PORT_CLIENT))
print("Connection to Slave successful...")
input()
operation = make_operation("ADD",op1=12,op2=34)

operation={
    **operation,
    "slave":slave_address,
    "token":token
}

operation_str = json.dumps(operation)

utils.sendMessageTCP(skt,operation_str)

response_from_slave_str = utils.receiveMessageTCP(skt)
print(response_from_slave_str)
response_from_slave = json.loads(response_from_slave_str)

result_op = response_from_slave["result"]
print("RESULT:",result_op)
