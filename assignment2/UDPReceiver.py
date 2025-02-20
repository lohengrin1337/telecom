#!/usr/bin/env python3

from socket import *
import time
import re

class UDPReceiver:
    """ UDP stream receiver 
        Capable of receiving text messages
        as UDP packet stream, and verifying sequence numbers """

    def __init__(self):
        """ Create UDP socket """
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._port = 12000
        self._timeout = 60
        self._next_sequence_num = 10001

    def set_port(self, port):
        self._port = port
        return self

    def set_timeout(self, timeout):
        self._timeout = timeout     # seconds
        return self

    def listen(self):
        """ Bind socket to port, and listen for incoming stream until timeout"""
        if not self._port:
            raise Exception("No port is currently set!")

        self._socket.bind(("", self._port))

        timeout = time.time() + self._timeout
        while time.time() < timeout:
            payload, _ = self._socket.recvfrom(2048)
            self._receive(payload.decode())

        print("timeout")
        self._close()

    def _receive(self, payload):
        """ Check all three parts of payload, and log results """
        # match sequence number, message and message terminator
        match = re.match(r"(\d{5});([A-Za-z]+)(#{4})", payload)

        if not match:
            # Format of payload is invalid
            print(f"ERROR: Payload corrupted! (expected seq: {self._next_sequence_num})")
            self._log(payload, corrupt=True)
            self._next_sequence_num += 1
            return

        seq_num = match.group(1)
        if not int(seq_num) == self._next_sequence_num:
            # Sequence number is out of order
            print(f"ERROR: Wrong sequence number: {seq_num}, expected: {self._next_sequence_num}")

            self._log(f"{seq_num} ({self._next_sequence_num})", invalid_seq=True)
            self._next_sequence_num += 1
            return

        # Payload arrived as expected
        self._log(seq_num)
        return

    def _log(self, message, corrupt=False, invalid_seq=False):
        """ Log sequence number, corrupted payload, or invalid seq """
        filename = "success.log"
        if corrupt:
            filename = "corrupt.log"
        if invalid_seq:
            filename = "invalid_seq.log"

        with open(filename, "a") as file:
            file.write(message)

    def _close(self):
        self._socket.close()


if __name__ == "__main__":
    timeout = 5

    udp_receiver = UDPReceiver()
    udp_receiver.set_timeout(timeout)
    udp_receiver.listen()
