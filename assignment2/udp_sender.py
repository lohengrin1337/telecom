#!/usr/bin/env python3

from sender import Sender
import socket

class UDPSender(Sender):
    """ UDP stream sender.
        Capable of sending text messages
        as UDP packet stream of variable
        frequency. """

    def _create_socket(self):
        """ Create UDP socket """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _connect(self):
        """ Implemented with tcp socket only """
        pass

    def _send(self, payload):
        """ Send payload into UDP socket """
        self._socket.sendto(payload, (self._receiver_name, self._receiver_port))

if __name__ == "__main__":
    rec_name = "127.0.0.1"
    rec_port = 12000
    freq = 15
    timeout = 30

    udp_sender = UDPSender()
    udp_sender.set_receiver(rec_name, rec_port).set_stream_frequency(freq).set_timeout(timeout)
    udp_sender.stream()
