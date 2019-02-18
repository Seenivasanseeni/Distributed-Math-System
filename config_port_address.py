'''Following are the constants for connecting to master'''
MASTER_UDP_ADDRESS="localhost"

#machine-protocol-action-component

#master listening
MASTER_UDP_LISTEN_CLIENT_PORT=9000
MASTER_UDP_LISTEN_SLAVE_PORT = 9001

MASTER_UDP_SEND_CLIENT_PORT=9002
MASTER_UDP_SEND_SLAVE_PORT = 9003

#clients should be using less number of ports as much as possible
CLIENT_UDP_SEND_PORT=9001
CLIENT_UDP_RECEIVE_PORT=9002

#slave address
SLAVE_CLIENT_SERVER_PORT = 9004
