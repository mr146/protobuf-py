#!/usr/local/bin/python2
import sys
import socket
from contract_pb2 import *
from helpers import *

invoice = read_invoice()
sock = socket.socket()
sock.connect(('localhost', 2233))
send_invoice(sock, invoice)
invoicesCount = receive_int(sock)
print '{0} invoices received'.format(invoicesCount)
for i in range(0, invoicesCount):
    print 'invoice {0}:'.format(i)
    invoice = receive_invoice(sock)
    print_invoice(invoice)
sock.close()