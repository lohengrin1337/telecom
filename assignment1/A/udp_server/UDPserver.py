# UDP Server
# Anders Nelsson BTH
# Example code from course book

from socket import *
serverPort = 12000

# create UDP socket and bind to specified port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ("The UDP server is ready to recieve")

while True:
    # read client's message and remember client's address (IP and port)
    message, clientAddress = serverSocket.recvfrom(2048)

    # Print message and client address
    print (message.decode())
    print (clientAddress)

    # change sentence to upper case letters
    modifiedMessage = message.decode().upper()

    # send back modified sentence to client using remembered address
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
