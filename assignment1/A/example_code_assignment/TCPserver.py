# TCP Server
# Anders Nelsson BTH
# Example code from course book

from socket import *
serverPort = 12000

# create TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))

# server starts listening for incoming TCP requests
serverSocket.listen(1)

print ('The TCP server is ready to receive')

while True:
    # server waits for incoming requests; new socket created on return
    connectionSocket, addr = serverSocket.accept()

    # read sentence of bytes from socket sent by the client
    sentence = connectionSocket.recv(1024).decode()

    # print unmodified sentance and client address
    print (sentence)

    # convert sentence to upper case
    capitalizedSentence = sentence.upper()

    # send back modified sentence over the TCP connection
    connectionSocket.send(capitalizedSentence.encode())
 
    # close the TCP connection; the welcoming socket continues
    connectionSocket.close()
