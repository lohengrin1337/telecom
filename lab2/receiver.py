#!/usr/bin/env python3

from abc import ABC, abstractmethod
import time
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
        """ Check sequence number and log results """
        seq_num = payload[:5]
        self._log(seq_num)

        if seq_num == str(self._next_sequence_num):
            self._valid_packets += 1
            self._next_sequence_num += 1
        else:
            print(f"Out of order: {seq_num}, expected {self._next_sequence_num}")
            self._invalid_packets += 1
            try:
                seq_num = int(seq_num)
                if seq_num > self._next_sequence_num:
                    # Act as if one or more previous packets are lost
                    self._next_sequence_num = seq_num + 1
                # else:
                    # Act as if current packet arrived late
                    # next seq = current seq
            except ValueError:
                # Payload starts with NaN
                self._next_sequence_num += 1

    def _log(self, sequence):
        """ Log sequence to file"""
        with open("sequence.log", "a") as file:
            file.write(sequence + "\n")

    @abstractmethod
    def _close(self):
        """ Close sockets in socket specific way """
        pass

    def _print_status(self):
        print("Packets received:", self._valid_packets + self._invalid_packets)
        print("Out of order:", self._invalid_packets)
