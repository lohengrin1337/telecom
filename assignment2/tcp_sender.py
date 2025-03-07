#!/usr/bin/env python3

from sender import Sender
from socket import socket, AF_INET, SOCK_STREAM

class TCPSender(Sender):
    """ TCP stream sender.
        Capable of sending text messages
        as TCP packet stream of variable
        frequency. """

    def _create_socket(self):
        """ Create TCP socket """
        self._socket = socket(AF_INET, SOCK_STREAM)

    def _connect(self):
        self._socket.connect((self._receiver_name, self._receiver_port))

    def _send(self, payload):
        """ Send payload into TCP socket """
        self._socket.send(payload.encode())

if __name__ == "__main__":
    # rec_name = "192.168.1.223"
    rec_name = "127.0.0.1"
    rec_port = 12000
    freq = 50
    timeout = 5

    tcp_sender = TCPSender()
    tcp_sender.set_receiver(rec_name, rec_port).set_stream_frequency(freq).set_timeout(timeout)
    tcp_sender.stream()
