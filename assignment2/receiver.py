#!/usr/bin/env python3

from abc import ABC, abstractmethod
import time
import re
from socket import timeout as socket_timeout

class Receiver:
    """ Abstract stream receiver.
        Capable of receiving text messages
        as packet stream, and processing payloads.
        Subclasses must implement _create_socket(), _prepare(),
        _receive() and _close() differently depending on socket type """

    def __init__(self):
        """ Create socket, set defaults """
        self._socket = None
        self._connection_socket = None
        self._port = 12000
        self._timeout = 60
        self._next_sequence_num = 10001
        self._valid_packets = 0
        self._invalid_packets = 0

        self._create_socket()

    @abstractmethod
    def _create_socket(self):
        """ Assign a socket of some type to _socket """
        pass

    def set_port(self, port):
        self._port = port
        return self

    def set_timeout(self, timeout):
        self._timeout = timeout     # seconds
        return self

    def listen(self):
        """ Prepare socket, and listen for incoming stream until timeout """
        if not self._port:
            raise Exception("No port is currently set!")

        print(f"Listening on port {self._port}. Timeout: {self._timeout}s")

        try:
            # Prepare socket to receive
            self._prepare()

            timeout = time.time() + self._timeout   # timeout for while loop
            self._socket.settimeout(1)  # refresh while loop at least every sec
            while time.time() < timeout:
                try:
                    payload = self._receive()
                    self._process(payload)
                except socket_timeout:
                    continue

        except ValueError:  # empty payload
            print("Sender closed connection")
        except ConnectionError as e:
            print(f"CONNECTION ERROR: {e}")
        except socket_timeout:
            # TCP socket timeout before established connection
            pass
        finally:
            self._close()
            self._print_status()

    @abstractmethod
    def _prepare(self):
        """ Prepare socket.
            Must be implemented by subclass. """
        pass

    @abstractmethod
    def _receive(self):
        """ Receive packet from socket.
            Must be implemented by subclass """
        pass

    def _process(self, payload):
        """ Check all three parts of payload, and log results """
        # match sequence number, message and message terminator
        match = re.match(r"(\d+);([A-Za-z]+)(#{4})", payload)

        if not match:
            # Format of payload is invalid
            print(f"ERROR: Payload corrupted! (expected seq: {self._next_sequence_num})")
            self._log(f"{payload} ({self._next_sequence_num})", corrupt=True)
            self._next_sequence_num += 1
            self._invalid_packets += 1
            return

        seq_num = match.group(1)
        if not int(seq_num) == self._next_sequence_num:
            # Sequence number is out of order
            print(f"ERROR: Wrong sequence number: {seq_num}, expected: {self._next_sequence_num}")
            self._log(f"{seq_num} ({self._next_sequence_num})", invalid_seq=True)
            self._next_sequence_num += 1
            self._invalid_packets += 1
            return

        # Payload arrived as expected
        self._log(seq_num)
        self._next_sequence_num += 1
        self._valid_packets += 1
        return

    def _log(self, message, corrupt=False, invalid_seq=False):
        """ Log sequence number, corrupted payload, and invalid seq num """
        if corrupt:
            with open("corrupt.log", "a") as file:
                file.write(message + "\n")
            if len(message) >= 5:
                message = message[:5]

        if invalid_seq:
            with open("invalid_seq.log", "a") as file:
                file.write(message + "\n")
            message = message[:5]

        with open("all_seq.log", "a") as file:
            file.write(message + "\n")

    @abstractmethod
    def _close(self):
        """ Close sockets in socket spesific way """
        pass

    def _print_status(self):
        print(f"Valid packets: {self._valid_packets}")
        print(f"Invalid packets: {self._invalid_packets}")
