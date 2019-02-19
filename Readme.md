#dist-Client
It is a client program for accessing a distributed system.

Procedure is as follows

Client should send a OR(operation request)

Master should receive and send a address of worker(slave)

open a new connection to slave

Get the data from slave

#Requirements
Python 3.6
[Add the versions of packages if used]

PORTS
for implementation purpose, it is recommended to use 9xxx for master 7xxx for client and 8xxx for slave
port constants are in this format
SERVER_PROTOCOL_ACTION_RECEIVER
