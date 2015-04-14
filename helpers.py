#!/usr/local/bin/python2
from struct import *
from contract_pb2 import *

def receive_bytes(socket, size):
    data = socket.recv(size)
    if len(data) == size:
        return data
    return data + read_bytes(socket, size - len(data))
    
def send_bytes(socket, data):
    socket.send(data)

def receive_int(socket):
    data = receive_bytes(socket, 4)
    return unpack('<i', data)[0]

def send_int(socket, value):
    data = pack('<i', value)
    socket.send(data)

def send_invoice(socket, invoice):
    result = invoice.SerializeToString()
    send_int(socket, len(result))
    send_bytes(socket, result)

def receive_invoice(socket):
    invoice = Invoice()
    size = receive_int(socket)
    invoice.ParseFromString(receive_bytes(socket, size))
    return invoice

def print_invoice(invoice):
    print '\tInvoice number: {0}'.format(invoice.invoiceNumber)
    print '\tInvoice id: {0}'.format(invoice.invoiceId)
    print '\tSupplier name: {0}'.format(invoice.supplierName)
    print '\tBuyer name: {0}'.format(invoice.buyerName)
    print '\tLicense id: {0}'.format(invoice.licenseId)
    index = 0
    for tradeItem in invoice.tradeItems:
        index = index + 1
        print '\tTrade item {0}:'.format(index)
        print '\t\tProduct code: {0}'.format(tradeItem.productCode)
        print '\t\tManufacturer name: {0}'.format(tradeItem.manufacturerName)
        print '\t\tQuantity: {0}'.format(tradeItem.quantity)

def read_invoice():
    invoice = Invoice()
    invoice.invoiceNumber = raw_input('Enter invoice number: ')
    invoice.invoiceId = raw_input('Enter invoice id: ')
    invoice.supplierName = raw_input('Enter supplier name: ')
    invoice.buyerName = raw_input('Enter buyer name: ')
    invoice.licenseId = raw_input('Enter license id (optional): ')
    tradeItemsCount = int(raw_input('Enter number of trade items: '))

    for i in range(0, tradeItemsCount):
        tradeItem = invoice.tradeItems.add()
        tradeItem.productCode = int(raw_input('Enter product code: '))
        tradeItem.manufacturerName = raw_input('Enter manufacturer name: ')
        tradeItem.quantity = float(raw_input('Enter quantity: '))
    return invoice