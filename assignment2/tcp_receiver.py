#!/usr/bin/env python3

from receiver import Receiver
from socket import socket, AF_INET, SOCK_STREAM

class TCPReceiver(Receiver):
    """ TCP stream receiver.
        Capable of receiving text messages
        as TCP packet stream, and verifying sequence numbers. """

    def _create_socket(self):
        """ Create TCP socket """
        return socket(AF_INET, SOCK_STREAM)

    def _prepare(self):
        """ Bind TCP socket to port, and listen """
        self._socket.bind(("", self._port))
        self._socket.settimeout(5)  # timeout for each recv call
        self._socket.listen(1)
        self._connection_socket, _ = self._socket.accept()

    def _receive(self):
        """ Accept request, and receive packet from socket """
        payload = self._connection_socket.recv(2048)
        return payload.decode()

    def _close(self):
        self._connection_socket.close()
        self._socket.close()


if __name__ == "__main__":
    timeout = 10

    tcp_receiver = TCPReceiver()
    tcp_receiver.set_timeout(timeout)
    tcp_receiver.listen()
