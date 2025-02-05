# TCP Client
# Anders Nelsson BTH
# Example code from course book

from socket import *
serverName = '127.0.0.1'
serverPort = 12000

# create TCP socket on client to use for connecting to remote server
clientSocket = socket(AF_INET, SOCK_STREAM)

# open the TCP connection
clientSocket.connect((serverName, serverPort))

# Input sentence from keyboard
sentence = input('Input lowercase sentence: ')

# send text over the TCP connection
# there's no need to specify server name & port
# sentence converted to bytes
clientSocket.send(sentence.encode())

# get modified sentence back from server
modifiedSentence = clientSocket.recv(1024)
print ('From Server:', modifiedSentence.decode())

# close the TCP connection
clientSocket.close()
