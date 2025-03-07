#!/usr/bin/env python3

from receiver import Receiver
from socket import socket, AF_INET, SOCK_DGRAM

class UDPReceiver(Receiver):
    """ UDP stream receiver.
        Capable of receiving text messages
        as UDP packet stream, and processing payload. """

    def _create_socket(self):
        """ Create UDP socket """
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def _prepare(self):
        """ Bind UDP socket to port """
        self._socket.bind(("", self._port))

    def _receive(self):
        """ Receive packet from socket """
        payload, _ = self._socket.recvfrom(2048)
        return payload.decode()

    def _close(self):
        self._socket.close()
        print("Socket closed")


if __name__ == "__main__":
    timeout = 35

    udp_receiver = UDPReceiver()
    udp_receiver.set_timeout(timeout)
    udp_receiver.listen()
