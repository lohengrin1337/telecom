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
    response = connectionSocket.recv(1024).decode()

    # print unmodified sentance and client address
    print (response)
 
    # close the TCP connection; the welcoming socket continues
    connectionSocket.close()
