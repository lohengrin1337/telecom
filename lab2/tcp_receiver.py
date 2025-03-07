#!/usr/bin/env python3

from receiver import Receiver
from socket import socket, AF_INET, SOCK_STREAM

class TCPReceiver(Receiver):
    """ TCP stream receiver.
        Capable of receiving text messages
        as TCP packet stream, and processing payload. """

    def _create_socket(self):
        """ Create TCP socket """
        self._socket = socket(AF_INET, SOCK_STREAM)

    def _prepare(self):
        """ Bind TCP socket to port, listen,
            create connection socket for incomming request """
        self._socket.bind(("", self._port))
        self._socket.settimeout(self._timeout)
        self._socket.listen(1)      # max 1 connection
        self._connection_socket, _ = self._socket.accept()

    def _receive(self):
        """ Accept request, and receive packet from socket """
        payload = self._connection_socket.recv(2048)
        if not payload:
            raise ValueError("Empty payload")   # sender closed connection
        return payload.decode()


    def _close(self):
        if self._connection_socket:
            self._connection_socket.close()
        self._socket.close()
        print("Sockets closed")


if __name__ == "__main__":
    timeout = 35

    tcp_receiver = TCPReceiver()
    tcp_receiver.set_timeout(timeout)
    tcp_receiver.listen()
