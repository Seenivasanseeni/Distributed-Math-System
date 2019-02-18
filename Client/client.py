import json
import socket
import utils

MASTER_ADDRESS = 'localhost'
MASTER_TCP_PORT = 9000

SLAVE_TCP_PORT = 9001


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

skt = socket.socket(type=socket.SOCK_STREAM)

skt.connect((MASTER_ADDRESS,MASTER_TCP_PORT))

utils.sendMessageTCP(skt,operation_str)

response_from_master_str = utils.receiveMessageTCP(skt)

response_from_master = json.loads(response_from_master_str)

token = response_from_master["token"]
slave_address = response_from_master["slave"]

skt.close()

#make a connection to slave
skt.connect((slave_address,SLAVE_TCP_PORT))
operation = make_operation("ADD",op1=12,op2=34)

operation={
    **operation,
    "slave":slave_address,
    "token":token
}

operation_str = json.dumps(operation)

utils.sendMessageTCP(skt,operation_str)


response_from_slave_str = utils.receiveMessageTCP(skt)

response_from_slave = json.loads(response_from_slave_str)

result_op = response_from_slave["result"]
print("RESULT:",result_op)
