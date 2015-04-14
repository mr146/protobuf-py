#!/usr/local/bin/python2
import sys
import socket
from contract_pb2 import *
from helpers import *

sock = socket.socket()
sock.bind(('', 2233))
sock.listen(1)
print 'connected!'
invoices = []
while True:
    connection, address = sock.accept()
    new_invoice = receive_invoice(connection)
    invoices = invoices + [new_invoice]
    send_int(connection, len(invoices))
    for invoice in invoices:
        send_invoice(connection, invoice)
    connection.close()
